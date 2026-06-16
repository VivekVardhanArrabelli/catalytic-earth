# Scaling Plan to 10k Mechanism Labels

Status: durable plan (2026-06-10). This is an entry point for future agents. Read
this first, then verify every claim below against its source before acting — see the
**"Sources & where to verify"** table near the end, which maps every element of this
plan to the exact `docs/decision_log.md` entry, module, artifact, or test. Two
grounding errors in the session that produced this plan (ESM2, and apo-vs-holo
promotion confirmability) both came from asserting decision-claims without first
reading the log. Treat any performance/promotion/capability claim as requiring a
decision-log citation.

---

## 2026-06-12 update — measured re-scope of the path (read this first)

Chronology note: the first dated update below is the current operational state. Older dated
updates retain their original wording for historical context and should not override newer entries.

**2026-06-16 automation update: PDE Hydrolase and strict tier-2 scouts are below apply gate.**
No authorized registry mutation was performed. A stale worker briefly appended the **17-row**
Hydrolase preview to the external registry; this was detected and reverted before commit, restoring
the SBL baseline of **7926** external rows. Frozen current702 remains unchanged at sha
`5eec9bef...`. Counts remain from the SBL apply: combined label surface **8628**, combined seed
surface **6932**, positive_bronze **6885**, OOS bronze **1696**, silver_confirmed **47**,
projected **0**.

The reviewed PDE EC 3.1.4 Hydrolase and ACT_SITE+catalytic lanes, plus stricter tier-2 GDPD/cyclic
source splits, are now wired in the source runner and covered by offline source-only guard tests.
EC, Hydrolase keyword, names, and active-site handles remain scope/fetch handles only. The reusable
row-guardrail audit checks preview rows before apply for UniProt namespace, bronze tier,
`automation_curated`, expected fingerprint/source tier, empty predictive evidence, required
excluded context, non-EC mechanism axes, and current702 duplicate-screen evidence.

Preview
`artifacts/v3_metal_independent_phosphodiesterase_ec314_hydrolase_preview_window0_120_current702_20260616_run0114.json`
admits **17** target rows from **120** reviewed candidates, with row guardrail audit
`artifacts/v3_metal_independent_phosphodiesterase_ec314_hydrolase_row_guardrail_audit_current702_20260616_run0114.json`
showing **0** problems. This is not apply authority: PDE would remain **17/100**. Strict tier-2
sample
`artifacts/v3_metal_independent_phosphodiesterase_tier2_preview_size20_current702_20260616_run1209.json`
admits **0** target rows from **40** unreviewed candidates and holds **6** off-target
`sam_methyltransferase` rows. Post-tier2 audits with suffix `20260616_run1209_post_tier2_scout`
still show PDE as the lone hole, novelty replay **7465** admit / **414** throttle / **47** reject,
and **0** existing lanes >=150 projected clean admits.

Follow-up strict tier-2 GDPD/cyclic preview
`artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_preview_size30_current702_20260616_run1235.json`
admits **28** target rows from **60** unreviewed candidates; row guardrail audit
`artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_row_guardrail_audit_current702_20260616_run1235.json`
shows **0** problem rows. This is still not apply authority because PDE would remain **28/100**.

Sharp reviewed-handle count scout
`artifacts/v3_metal_independent_phosphodiesterase_sharp_handle_count_scout_current702_20260616_run1207.json`
shows no obvious reviewed-source rescue. Broad Hydrolase has **490** raw reviewed rows but already
previewed to **17** admits; the best sharper non-baseline handle
`actsite_catalytic_non_metal` has only **119** raw rows before disambiguation/novelty.
Bounded ACT_SITE+catalytic preview
`artifacts/v3_metal_independent_phosphodiesterase_actsite_catalytic_preview_size40_current702_20260616_run1218.json`
admitted only **2** target rows from **40** reviewed candidates and had **0** row-guardrail
problems.

Next action: do not apply the 17-row Hydrolase, 2-row ACT_SITE, or 28-row GDPD/cyclic previews,
and do not rerun the same broad reviewed PDE windows. Either design a genuinely sharper
mechanism-bearing PDE source wall that can close the 100 floor, or move beyond reviewed Swiss-Prot
only through count scout, preregistration if needed, non-destructive preview, row audit,
novelty/governor/dedup/cap replay, leakage/source-contract tests, and explicit apply after the
batch gate passes.

**2026-06-16 automation update: SBL 46fp tier-2 floor batch applied; PDE remains the lone
hole.** Treat this as the newest operational state for bronze scaleout. Hard safety remains green,
frozen current702 stayed byte-unchanged at sha `5eec9bef...`, and growth happened only through the
sharded external bronze registry. The current positive fingerprint universe is now
`label_factory_v1_46fp` with **46** fingerprints and **43** ontology families. Counted label
counters are now: external rows **7926**, external seed **6702**, external OOS **1224**, external
silver **30**, combined label surface **8628**, combined seed surface **6932**, positive_bronze
**6885**, OOS bronze **1696**, silver_confirmed **47**, projected **0**.

`serine_beta_lactamase` is now a guarded mechanism-first lane, not a predictive feature path. EC
3.5.2.6, protein names, active-site/query handles, UniProt prose, and reaction text are
scope/admission excluded context. Counted corroboration is non-EC mechanism evidence:
serine-beta-lactamase family/domain context, beta-lactam hydrolysis reaction/participant evidence,
and Ser/Lys/Glu active-site context. Metallo/zinc beta-lactamases, PBPs/DD-peptidases,
beta-lactam synthases, generic amidohydrolases, side-EC, EC-only, and multi-fingerprint rows are
held, and `predictive_evidence` remains empty. The lane includes fingerprint/ontology/deploy
context, source runner `src/catalytic_earth/serine_beta_lactamase_sourcing.py`, script
`scripts/source_serine_beta_lactamase_family.py`, factory wiring, focused tests, and 46fp
hard-negative preregistration
`artifacts/v3_external_hard_negative_next_tranche_preregistration_46fp_1025.json`.

Non-destructive preview
`artifacts/v3_serine_beta_lactamase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260616_run0014.json`
fetched **240** unreviewed tier-2 rows, found **115** target mechanism-corroborated labels,
admitted **106** after novelty/cap replay, held **0** off-target fingerprint matches, and reached
the **100** floor. Row audit
`artifacts/v3_serine_beta_lactamase_tier2_row_guardrail_audit_current702_20260616_run0014.json`
found **0** problem rows. Explicit reuse-preview apply appended **106** rows (**7820 -> 7926**) and
verified the frozen current702 sha before/after.

Post-apply artifacts:
`artifacts/v3_coverage_redundancy_audit_current702_20260616_run0014_post_sbl_apply.json`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0014_post_sbl_apply.json`,
`artifacts/v3_high_yield_family_lane_factory_current702_20260616_run0014_post_sbl_apply.json`,
`artifacts/v3_mechanism_representation_loop_current702_20260616_run0014_post_sbl_apply.json`,
`artifacts/v3_evidence_handle_expansion_current702_20260616_run0014_post_sbl_apply.json`,
`artifacts/v3_breadth_feasibility_scout_current702_20260616_run0014_post_sbl_apply.json`, and
`artifacts/v3_post_sbl_source_strategy_current702_20260616_run0014.json`. Coverage still shows
`metal_independent_phosphodiesterase` as the lone hole/under-floor fingerprint, fingerprint Gini
**0.1948**, and only `metal_dependent_hydrolase` over cap. Novelty replay is **7465** admit /
**414** throttle / **47** reject across **7926** expansion rows. The factory has **0** ready
existing lanes >=150; top projected clean admits are **77** under current handles. Evidence-handle
refresh still shows **741** capped reachable uplift in handle-blocked families, not apply
authority. Breadth feasibility projects reviewed Swiss-Prot clean-only positives to **9573**,
leaving a **427** positive gap to 10k before further diversity discounts.

The representation loop now includes source-free `bc_beta_lactam_hydrolysis` so SBL does not
collapse into generic ester/Ser-His hydrolase chemistry. The post-apply representation loop remains
leakage-safe with **6702** seed labels, LOO self-consistency **0.7635**, and SBL
self-consistency **1.0**.

Next action: do not source more SBL without a new reaction-diversity split. Do not retry broad PDE
EC/name handles, the 7-row PLD preview, or terpene window170. Build a sharper
`metal_independent_phosphodiesterase` source wall that can plausibly close the 100 floor, or move
to a source-tier expansion strategy beyond reviewed Swiss-Prot through count scout,
preregistration if needed, non-destructive preview, row audit, novelty/governor/dedup/cap replay,
leakage/source-contract validation, and explicit apply only if the batch gate is met.

**2026-06-15 automation update: PDE PLD source-wall scout is valid but subfloor; no registry
mutation.** Treat this as the newest operational state for bronze scaleout. Hard safety remains
green, frozen current702 stayed byte-unchanged at sha `5eec9bef...`, and no registry rows were
applied. Counted label counters remain: external rows **7820**, external seed **6596**, external
OOS **1224**, external silver **30**, combined label surface **8522**, combined seed surface
**6826**, positive bronze **6779**, OOS bronze **1696**, silver_confirmed **47**, projected **0**.

The remaining hole is still `metal_independent_phosphodiesterase`. The run added a narrow
phospholipase-D split to the PDE source wall: `phospholipase D` family text plus explicit
hydrolytic phosphodiester reaction participants such as phosphocholine,
phosphoethanolamide/glycosylinositol, and glycero-3-phosphate. EC 3.1.4 and protein/reaction text
stay scope/admission excluded context, phospholipase C remains a boundary hold, metal rows remain
held, and `predictive_evidence` remains empty.

Non-destructive PLD preview
`artifacts/v3_metal_independent_phosphodiesterase_phospholipase_d_preview_current702_20260615_run2314.json`
fetched **22** reviewed rows, produced **7** target mechanism-corroborated labels, held **4**
off-target metallophosphoesterase/nuclease rows, and admitted **7** novelty-safe rows. Row audit
`artifacts/v3_metal_independent_phosphodiesterase_phospholipase_d_row_guardrail_audit_current702_20260615_run2314.json`
found **0** problem rows, but this is far below the 100-floor closure gate and was not applied.

The run also added timeout-safe live fetching to
`scripts/source_terpene_cyclase_synthase_family.py` and the terpene sourcing writer. Bounded
terpene cap-close preview
`artifacts/v3_terpene_cyclase_synthase_capclose_window170_preview_current702_20260615_run2314.json`
fetched **138** rows but admitted **0** novelty-safe rows, so no cap-close apply was available.
Fresh coverage/novelty/factory artifacts with `run2314_pre_lane` still show PDE as the lone hole,
novelty replay **7359** admit / **414** throttle / **47** reject, **0** ready existing lanes
>=150, and top current-handle clean supply **77**. Evidence-handle refresh
`artifacts/v3_evidence_handle_expansion_current702_20260615_run2314.json` reports reviewed
source-wall headroom but only for balanced/capped families that must not be padded without a
family-specific gate.

Next-lane source-tier scout
`artifacts/v3_serine_beta_lactamase_source_tier_scout_current702_20260615_run2314.json` found
reviewed serine beta-lactamase supply below the usual batch gate (**147** exact/name rows, **132**
active/binding-site rows), but strict unreviewed tier-2 active-site/reaction supply is large
(**1854** rows). This is only future-lane evidence: it requires a new guarded
serine-beta-lactamase fingerprint/ontology/source runner, OOS preregistration, metallo/zinc and
PBP/DD-peptidase/amidohydrolase holds, row audit, and source-contract/leakage tests before any
apply.
Design artifact
`artifacts/v3_serine_beta_lactamase_build_plan_current702_20260615_run2314.json` records the
no-apply build sequence and mechanism contract if this lane is used after another PDE attempt.

Next action: do not apply the 7-row PLD preview, do not retry terpene window170, and do not reuse
the broad PDE EC/name handles. Build a sharper mechanism-bearing PDE split capable of closing the
100 floor, or design a new high-yield family/source-tier lane through the full OOS/preregistration,
non-destructive preview, row audit, novelty/governor/dedup/cap, leakage, and source-contract gates.

**2026-06-15 automation update: SDR 45fp floor batch applied; PDE remains the lone hole.** Treat
this as the newest operational state for bronze scaleout. Hard safety remains green, frozen
current702 stayed byte-unchanged at sha `5eec9bef...`, and growth happened only through the
sharded external bronze registry. The current positive fingerprint universe is now
`label_factory_v1_45fp` with **45** fingerprints and **42** ontology families. Counted label
counters are now: external rows **7820**, external seed **6596**, external OOS **1224**, external
silver **30**, combined label surface **8522**, combined seed surface **6826**, positive bronze
**6779**, OOS bronze **1696**, silver_confirmed **47**, projected **0**.

`short_chain_dehydrogenase_reductase` is now a guarded mechanism-first lane, not a predictive
feature path. EC 1.1.1, SDR names, UniProt prose, and source handles are scope/admission excluded
context. Counted corroboration is non-EC mechanism evidence: SDR family/domain, NAD(P)
cosubstrate, Rhea redox reaction/participant, and active/binding-site context when present.
AKR/MDR/ALDH/flavin/metal redox boundary rows are held, and `predictive_evidence` remains empty.
The lane includes fingerprint/ontology/deploy context, source runner
`src/catalytic_earth/short_chain_dehydrogenase_reductase_sourcing.py`, script
`scripts/source_short_chain_dehydrogenase_reductase_family.py`, factory wiring, focused tests, and
45fp hard-negative preregistration
`artifacts/v3_external_hard_negative_next_tranche_preregistration_45fp_1025.json`.

Non-destructive preview
`artifacts/v3_short_chain_dehydrogenase_reductase_sourcing_preview_named220_current702_20260615_run2213.json`
fetched **220** reviewed UniProt rows, found **103** target mechanism-corroborated labels, admitted
**100** after novelty/cap replay, held **0** off-target rows, and reached the **100** floor. Row
audit
`artifacts/v3_short_chain_dehydrogenase_reductase_row_guardrail_audit_current702_20260615_run2213.json`
found **0** problem rows. Explicit reuse-preview apply appended **100** rows (**7720 -> 7820**)
and verified the frozen current702 sha before/after.

Post-apply planning artifacts:
`artifacts/v3_coverage_redundancy_audit_current702_20260615_run2213_post_sdr_apply.json`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260615_run2213_post_sdr_apply.json`,
`artifacts/v3_high_yield_family_lane_factory_current702_20260615_run2213_post_sdr_apply.json`, and
`artifacts/v3_mechanism_representation_loop_current702_20260615_run2213_post_sdr_apply.json`, with
non-mutating promotion/family-target refreshes in
`artifacts/v3_bronze_silver_promotion_preview_current702_20260615_run2213_post_sdr_apply.json` and
`artifacts/v3_family_set_expansion_targets_current702_20260615_run2213_post_sdr_apply.json`.
Coverage still shows `metal_independent_phosphodiesterase` as the lone hole/under-floor
fingerprint, fingerprint Gini **0.1944**, and only `metal_dependent_hydrolase` over cap. Novelty
replay is **7359** admit / **414** throttle / **47** reject across **7820** expansion rows. The
factory has **0** ready existing lanes >=150; top projected clean admits are **77** under current
handles. Representation loop remains leakage-safe with LOO self-consistency **0.7576**; SDR is
separable (**0.95**), while generic NAD(P) dehydrogenase now has a documented source-free
reaction-chemistry ceiling against SDR.

Next action: do not source more SDR, APH, or the same PDE windows. The remaining safe
bronze-scaleout path is a materially sharper mechanism-bearing PDE source wall beyond EC/name
counts, or a new high-yield family/source-tier strategy that goes through OOS preregistration if
needed, non-destructive preview, row guardrail audit, novelty/governor/dedup/cap replay,
leakage/source-contract validation, and explicit apply only if the clean batch gate is met.

**2026-06-15 automation update: APH tier-2 source-handle batch applied; PDE remains the lone
hole.** Treat this as the newest operational state for bronze scaleout. Hard safety remains green,
frozen current702 stayed byte-unchanged at sha `5eec9bef...`, and growth happened only through the
sharded external bronze registry. The current positive fingerprint universe remains
`label_factory_v1_44fp` with **44** fingerprints and **41** ontology families. Counted label
counters are now: external rows **7720**, external seed **6496**, external OOS **1224**, external
silver **30**, combined label surface **8422**, combined seed surface **6726**, positive bronze
**6679**, OOS bronze **1696**, silver_confirmed **47**, projected **0**.

APH tier-2 sourcing is guarded admission evidence, not predictive evidence. The APH runner now has
unreviewed tier-2 lane switches and a fail-closed `source_tier_2` mode requiring at least three
independent non-EC mechanism axes; EC, protein name, query handles, and reaction text stay in
excluded context. The preview
`artifacts/v3_aminoglycoside_phosphotransferase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260615.json`
fetched **240** rows, found **239** target mechanism-corroborated labels, admitted **150** after
novelty/cap replay, held **70** at cap, and had **0** off-target holds. Row audit
`artifacts/v3_aminoglycoside_phosphotransferase_tier2_row_guardrail_audit_current702_20260615.json`
found **0** problem rows. Explicit reuse-preview apply appended **150** rows (**7570 -> 7720**)
and verified the frozen current702 sha before/after.

Post-apply planning artifacts:
`artifacts/v3_coverage_redundancy_audit_current702_20260615_post_aph_tier2_apply.json`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_aph_tier2_apply.json`,
`artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_aph_tier2_apply.json`, and
`work/metal_independent_phosphodiesterase_post_aph_source_strategy_current702_20260615.md`.
Coverage now shows `metal_independent_phosphodiesterase` as the lone hole/under-floor fingerprint,
fingerprint Gini **0.1944**, and only `metal_dependent_hydrolase` over cap. Novelty replay is
**7259** admit / **414** throttle / **47** reject across **7720** expansion rows. The factory has
**0** ready existing lanes >=150; top projected clean admits are
`short_chain_dehydrogenase_reductase` at **84**, and PDE projects only **34** under current handles.
The post-APH PDE exact-EC distribution scout
`artifacts/v3_metal_independent_phosphodiesterase_exact_ec_distribution_scout_current702_20260615_post_aph_apply.json`
shows exact cyclic-nucleotide PDE splits remain subscale after the non-metal filter (largest exact
cyclic split **18**) while broad EC/name windows are boundary-heavy.
Fallback source-handle scout
`artifacts/v3_evidence_handle_expansion_current702_20260615_post_aph_apply.json` probed **6**
families and found **741** capped reachable positive-bronze uplift from better reviewed handles
across **4** handle-blocked families. This is source-wall headroom, not additive supply: NAD(P) and
broad oxidoreductase pools overlap and must be split into family-specific capped lanes before
mutation.

Next action: do not source more APH and do not pad the 14-row reviewed PDE preview or 0-row PDE
tier-2 preview. The remaining safe bronze-scaleout path is either a new mechanism-bearing PDE
source wall beyond EC/name counts, or a split high-yield source-tier/family strategy such as
SDR/AKR or serine beta-lactamase that goes through OOS preregistration if needed, non-destructive
preview, row guardrail audit, novelty/governor/dedup/cap replay, leakage/source-contract
validation, and explicit apply only if the clean batch gate is met.

**2026-06-15 automation update: APH 44fp infrastructure built; corrected source wall is
subscale, no registry mutation.** Treat this as the newest operational state for bronze scaleout.
Hard safety remains green, frozen current702 was not written, and no external bronze labels were
applied. The current positive fingerprint universe is now `label_factory_v1_44fp` with **44**
fingerprints and **41** ontology families. Counted label counters are unchanged from the
N-ribosyl apply: external rows **7570**, combined label surface **8272**, combined seed surface
**6576**, positive bronze **6529**, OOS bronze **1696**, silver_confirmed **47**, projected **0**.

`aminoglycoside_phosphotransferase` now has guarded lane infrastructure:
`src/catalytic_earth/aminoglycoside_phosphotransferase_sourcing.py`,
`scripts/source_aminoglycoside_phosphotransferase_family.py`, fingerprint
`aminoglycoside_phosphotransferase`, ontology family `aminoglycoside_phosphoryl_transfer`,
deploy context, coverage/governor signature, factory wiring, focused tests, and 44fp
hard-negative preregistration
`artifacts/v3_external_hard_negative_next_tranche_preregistration_44fp_1025.json`.

Important correction: live UniProt inspection showed EC `2.7.1.130` and `2.7.1.192` are not APH
rows; they are lipid-A and PTS MurNAc kinase surfaces. APH scope is restricted to `2.7.1.95`,
`2.7.1.72`, `2.7.1.87`, `2.7.1.119`, and `2.7.1.163`, with APH family/name plus ATP/Mg,
aminoglycoside phosphorylation, active-site, or binding-site mechanism evidence. EC remains
scope-only and never a counted corroborator.

Corrected live preview
`artifacts/v3_aminoglycoside_phosphotransferase_sourcing_preview_corrected_active_binding_bounded50_current702_20260615.json`
fetched **18** reviewed rows and admitted **17** novelty-safe APH rows, below the >=150 clean-admit
batch gate. No apply was performed. Current planning artifacts:
`artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_aph_44fp_infra.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260615_post_aph_44fp_infra.json`, and
`artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_aph_44fp_infra.json`.
Coverage shows holes `aminoglycoside_phosphotransferase` and
`metal_independent_phosphodiesterase`; the factory has **0** ready existing lanes >=150 and top
projected clean admits `short_chain_dehydrogenase_reductase` at **84**.

Next action: do not apply the 17-row APH preview. Move to a higher-yield mechanism-first source
strategy, likely SDR/AKR or another source tier/family that can plausibly clear >=150 after
source-wall, OOS preregistration if needed, non-destructive preview, row guardrail audit,
novelty/governor/dedup/cap replay, leakage/source-contract validation, and explicit apply.

**2026-06-15 automation update: metal-independent PDE 43fp infrastructure built; tested source
handles are below the apply gate.** Treat this as the newest operational state for bronze
scaleout. Hard safety remains green, frozen current702 was not written, and no external bronze
labels were applied. The current positive fingerprint universe is now `label_factory_v1_43fp` with
**43** fingerprints and **40** ontology families. Counted label counters are unchanged from the
N-ribosyl apply: external rows **7570**, combined label surface **8272**, combined seed surface
**6576**, positive bronze **6529**, OOS bronze **1696**, silver_confirmed **47**, projected **0**.

The `metal_independent_phosphodiesterase` lane now has the missing infrastructure:
`src/catalytic_earth/metal_independent_phosphodiesterase_sourcing.py`,
`scripts/source_metal_independent_phosphodiesterase_family.py`, fingerprint
`metal_independent_phosphodiesterase`, ontology family
`metal_independent_phosphodiester_hydrolysis`, deploy context, coverage/governor signature,
factory wiring, focused tests, and 43fp hard-negative preregistration
`artifacts/v3_external_hard_negative_next_tranche_preregistration_43fp_1025.json`. EC 3.1.4 /
4.6.1 and keyword/name/query handles are scope/admission context only; metal absence is a filter,
not evidence; predictive evidence stays empty.

Live source work shows this lane should not be applied under the currently tested handles. The
reviewed cursor preview
`artifacts/v3_metal_independent_phosphodiesterase_sourcing_preview_cursor_pages4_size80_current702_20260615.json`
fetched **265** reviewed rows, found **18** target mechanism-corroborated labels, and admitted only
**14** novelty-safe labels. Alternate reviewed handles fetched **130** rows with **0** targets and
**0** admits. Tier-2 PDE count scouts were large, but the tier-2 preview
`artifacts/v3_metal_independent_phosphodiesterase_tier2_sourcing_preview_cursor_pages2_size100_current702_20260615.json`
fetched **400** rows with **0** target labels, **0** admits, **186** off-target holds, and **197**
`trust_tier_corroboration_insufficient` holds. Strategy note:
`work/metal_independent_phosphodiesterase_43fp_source_strategy_current702_20260615.md`.

Post-infrastructure planning artifacts:
`artifacts/v3_coverage_redundancy_audit_current702_20260615_post_pde_43fp_infra.json`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_pde_43fp_infra.json`, and
`artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_pde_43fp_infra.json`.
Coverage now shows `metal_independent_phosphodiesterase` as the lone hole/under-floor fingerprint,
Gini **0.1974**, and only `metal_dependent_hydrolase` over cap. Novelty replay is **7109** admit /
**414** throttle / **47** reject across **7570** expansion rows. The factory reports **0** ready
existing lanes >=150 and no high-yield blocked lanes under current handles; top projected clean
admits are `short_chain_dehydrogenase_reductase` at **84**.

Next action: do not retry the same PDE UniProt handles for mass growth and do not pad the 14-row
preview. Either design a materially sharper PDE source split, or move to a higher-yield
source-handle/source-tier strategy such as SDR/AKR with a family-specific mechanism-first source
wall, fresh OOS preregistration if the fingerprint universe changes, non-destructive preview, row
guardrail audit, novelty/governor/dedup/cap replay, leakage/source-contract validation, and apply
only if the batch gate is met.

**2026-06-15 automation update: N-ribosyl hydrolase cursor batch applied; next lane is
metal-independent phosphodiesterase.** Treat this as the newest operational state for bronze
scaleout. Hard safety remains green, frozen current702 was not written, and growth happened only in
the sharded external registry. The current positive fingerprint universe remains
`label_factory_v1_42fp` with **42** fingerprints and **39** ontology families. Counted label
counters are now: external rows **7570**, combined label surface **8272**, combined seed surface
**6576**, positive bronze **6529**, OOS bronze **1696**, silver_confirmed **47**, projected **0**.

The source unlock was reliable UniProt Link-header pagination in
`src/catalytic_earth/adapters.py`, wired into `scripts/source_n_ribosyl_hydrolase_family.py` with
`--use-query-cursor-pagination` and `--query-pages-per-lane`; the script timeout wrapper now reads
large child-process payloads before join, avoiding false timeout blockers. Cursor preview
`artifacts/v3_n_ribosyl_hydrolase_sourcing_preview_cursor_synonym_pages5_size40_current702_20260615.json`
fetched **200** reviewed rows, produced **181** mechanism-corroborated N-ribosyl labels, admitted
**150** novelty-safe rows, and held **31** at cap. Row guardrail audit
`artifacts/v3_n_ribosyl_hydrolase_row_guardrail_audit_current702_20260615_cursor_synonym_pages5_size40.json`
found **0** problems. The explicit reuse-preview apply appended **150** rows (**7420 -> 7570**),
skipped **0** duplicates, and verified the frozen current702 sha before/after.

Post-apply planning artifacts:
`artifacts/v3_coverage_redundancy_audit_current702_20260615_post_n_ribosyl_apply.json`,
`artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_n_ribosyl_apply.json`, and
`artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_n_ribosyl_apply.json`.
Coverage now has no holes/under-floor fingerprints, Gini **0.1783**, and only
`metal_dependent_hydrolase` over cap. Novelty replay is **7109** admit / **414** throttle / **47**
reject across **7570** external rows. The next high-yield lane is
`metal_independent_phosphodiesterase`, projected **150** clean admits, requiring a full 43fp gated
path before any apply.

Post-rebase representation safety is green after a source-free reaction-center repair:
N-ribosyl Rhea equations now fire `bc_n_glycosidic_hydrolysis` when ribose or
ribose-5-phosphate plus a nucleobase is produced. This fixed the post-apply/rebase real-registry
representation failure without using EC/name/prose/lane features: overall leave-one-out
self-consistency is **0.7598**, `n_ribosyl_hydrolase` is **0.9933**, and carbohydrate
`glycoside_hydrolase` remains **0.8133**.

Post-apply next-lane reconnaissance warns against using broad first windows alone:
`artifacts/v3_metal_independent_phosphodiesterase_source_wall_scout_current702_20260615_post_n_ribosyl_apply.json`
fetched **68** rows but produced only **1** target preview label. Source-handle count scout
`artifacts/v3_metal_independent_phosphodiesterase_source_handle_count_scout_current702_20260615_post_n_ribosyl_apply.json`
found better candidate handles for the future runner: cyclic AMP/GMP catalytic-activity EC 3.1.4
(**121** reviewed matches), phosphodiesterase hydrolase non-metal keyword (**224**), and EC 3.1.4
active/binding-site handles (**718**). EC 4.6.1 is high-count (**1389**) but likely
cyclase-boundary-heavy.

Additional previews show the first obvious handle expansions remain subscale:
`artifacts/v3_metal_independent_phosphodiesterase_targeted_source_wall_scout_current702_20260615_post_n_ribosyl_apply.json`
fetched **157** rows but yielded only **13** target / **11** novelty-admitted preview rows, and
cursor-paged active/binding-site, hydrolase non-metal, and cyclic-nucleotide name handles in
`artifacts/v3_metal_independent_phosphodiesterase_cursor_source_wall_scout_current702_20260615_post_n_ribosyl_apply.json`
fetched **244** rows but yielded only **18** target / **14** novelty-admitted preview rows. These
are source-wall evidence only. They argue for sharper lane splits or additional mechanism-bearing
source handles before an apply-sized 43fp preview.

Next action: do not continue N-ribosyl now that it is capped at 150. Build
`metal_independent_phosphodiesterase` as the 43rd fingerprint: add fingerprint and ontology node,
refresh/freeze the hard-negative OOS preregistration for `label_factory_v1_43fp` before candidate
selection, implement the reviewed-UniProt runner with improved source handles, run
non-destructive preview + row guardrail audit, then apply only if novelty, governor, dedup, cap,
source-contract, leakage, and frozen-SHA gates pass.

**2026-06-15 automation update: N-ribosyl hydrolase 42fp infrastructure built; live aggregate
blocked below batch gate.** Treat this as the newest operational state for bronze scaleout. Hard
safety remains green, frozen current702 was not written, and no external bronze labels were
applied. The current positive fingerprint universe is now `label_factory_v1_42fp` with **42**
fingerprints and **39** ontology families. Counted label counters are unchanged from the prior
Ser/Thr apply: external rows **7420**, combined label surface **8122**, combined seed surface
**6426**, positive bronze **6379**, OOS bronze **1696**, silver_confirmed **47**, projected **0**.

The `n_ribosyl_hydrolase` lane now has the missing infrastructure:
`src/catalytic_earth/n_ribosyl_hydrolase_sourcing.py`,
`scripts/source_n_ribosyl_hydrolase_family.py`, fingerprint `n_ribosyl_hydrolase`, ontology
family `n_glycosidic_bond_hydrolysis`, 42fp OOS preregistration
`artifacts/v3_external_hard_negative_next_tranche_preregistration_42fp_1025.json`, factory wiring,
coverage/governor signatures, deploy context, and focused tests. EC 3.2.2 remains scope-only;
N-ribosyl/nucleosidase names and keyword handles are admission/source context only and are not
predictive features. Counted corroboration requires non-EC mechanism evidence, especially
N-glycosidic hydrolysis Rhea/reaction-participant evidence plus family/name context.

Live non-destructive sourcing found **61** unique novelty-safe N-ribosyl rows after synonym-handle
expansion and aggregate dedup/novelty/cap replay. Row guardrails passed with **0** problem rows, but
the batch is below the **150** clean-admit mutation gate, so no apply was performed. Do not use the
historical `apply_candidate` filenames as authority: their corrected statuses are
`non_destructive_aggregate_blocked_below_150_no_apply` and
`row_guardrails_pass_but_batch_gate_blocks_apply`. Offset-paged UniProt synonym windows had a raw
mechanism-corroborated sum of **166** but overlapped earlier accessions, leaving only **61** unique
labels; next source work should add reliable cursor pagination or a stronger reviewed source path
before any registry mutation.

Post-infrastructure planning artifacts:
`artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_n_ribosyl_infra.json`,
`artifacts/v3_coverage_redundancy_audit_current702_20260615_post_n_ribosyl_infra.json`, and
`artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_n_ribosyl_infra.json`.
Coverage now shows `n_ribosyl_hydrolase` as the lone under-floor/hole until a clean >=150-row
aggregate exists. If reliable N-ribosyl supply is exhausted, pivot to
`metal_independent_phosphodiesterase` as the next new-fingerprint lane with a fresh preregistration
for the then-current fingerprint universe.

**2026-06-15 automation update: discovery-compass source walls added; registry unchanged.**
Treat this as the newest operational state for bronze scaleout. Hard safety remains green, the
current positive universe remains `label_factory_v1_41fp`, frozen current702 was not written, and
no labels/fingerprints/ontology nodes were applied.

The high-yield factory now includes the 2026-06-15 discovery/de novo compass lanes and reports
**0** ready existing lanes >=150. The top two high-yield candidates are no longer blocked on source
wall design: both have tested preview-only rules in
`src/catalytic_earth/external_cofactor_ec_disambiguation.py`, while fingerprint, ontology, OOS
preregistration, source runner, preview, row audit, and explicit apply are still required.

- `n_ribosyl_hydrolase`: reviewed non-EC-corroborated supply **1991**, projected clean admits
  **150**, design-only preregistration
  `artifacts/v3_n_ribosyl_hydrolase_lane_preregistration_current702_20260615_discovery_compass.json`.
- `metal_independent_phosphodiesterase`: reviewed non-EC-corroborated supply **1129**, projected
  clean admits **150**, design-only preregistration
  `artifacts/v3_metal_independent_phosphodiesterase_lane_preregistration_current702_20260615_discovery_compass.json`.

EC 3.2.2 / 3.1.4 / 4.6.1 remain scope-only and never counted. Metal-independent
phosphodiesterase treats metal presence as a hold/filter; metal absence is not evidence. Next
registry mutation should build `n_ribosyl_hydrolase` through the 42fp gated path, not pad SDR at
84 admits and not apply from the preview-only source wall alone. Rebased context:
`work/next_instance_representation_separability_fix_spec.md` is now an active prerequisite before
more ester-hydrolase, phosphatase, or NAD-redox-subtype sourcing, which further argues against SDR
padding before the representation fix.

**2026-06-14 automation update: Ser/Thr protein phosphatase bronze batch applied after Rhea
reaction-token fix.** Treat this as the latest counted-registry state, superseded for lane
selection by the 2026-06-15 discovery-compass source-wall update above. Registry-size safety remains
green: the external registry is still a small sharded manifest plus shard files below the per-file
safety threshold. Frozen current702 stayed byte-unchanged at sha `5eec9bef...`.

The Ser/Thr runner's source wall now recognizes curated protein-substrate reaction forms such as
`O-phospho-L-seryl-[protein] + H2O = L-seryl-[protein] + phosphate` and the threonyl analog as
mechanism reaction evidence. EC 3.1.3.16/48 remains scope/fetch context only and is never a counted
corroborator. After the fix, contiguous bounded windows through offset 220-260 were aggregated:
**743** fetched candidates, **170** unique mechanism-corroborated Ser/Thr candidates, **112**
novelty-safe admits after aggregate replay, **58** novelty-throttled/rejected rows, and **2**
off-target metallophosphomonoesterase holds. Row guardrail audit passed with **0** problems.

Applied result: external registry **7308 -> 7420** rows; combined label surface **8010 -> 8122**.
Current honest counters: external seed **6196**, external OOS **1224**, external silver **30**,
combined seed surface **6426**, combined OOS **1696**, positive bronze **6379**,
silver_confirmed **47**, projected **0**. Remaining seed gap to 10k is **3574**.

Post-apply coverage/novelty are green: no holes, Gini **0.1807**, novelty replay **6959** admit /
**414** throttle / **47** reject. The high-yield factory now reports **0** ready existing lanes
with >=150 projected clean admits; top candidate is `short_chain_dehydrogenase_reductase` at **84**
projected clean admits and is design-only preregistered in
`artifacts/v3_short_chain_dehydrogenase_reductase_lane_preregistration_current702_20260614_post_ser_thr_apply.json`.
Do not mutate registry again for subscale growth unless a source-handle or external-source change
raises projected clean supply; continue silver geometry/residue-mapping quality work in parallel.
Current silver blocker detail: all **202** silver-ready rows have verified local holo coordinates,
but a full residue-mapping preview mapped **0** rows because **82** lack mmCIF alignment tables,
**4** lack exact residues, and **116** had no residue positions mapped.
Post-apply evidence-handle scout still finds **741** reachable positive-bronze uplift from better
handles, while breadth feasibility projects reviewed Swiss-Prot clean-only positive bronze to
**9067**, leaving a **933** positive gap; reaching 10k positive bronze still requires source
expansion beyond reviewed Swiss-Prot or a broader target definition that keeps positive, OOS,
silver, and projected counters separate.

**2026-06-14 automation update: Ser/Thr protein phosphatase runner built; live sourcing blocked.**
Treat this as the newest operational state. Registry-size safety remains green and frozen
current702 stayed byte-unchanged at sha `5eec9bef...`. The current positive fingerprint universe is
now `label_factory_v1_41fp`.

The guarded Ser/Thr protein phosphatase lane now exists:
`src/catalytic_earth/ser_thr_protein_phosphatase_sourcing.py`,
`scripts/source_ser_thr_protein_phosphatase_family.py`, new fingerprint
`ser_thr_protein_phosphatase`, ontology family
`dinuclear_metal_phosphoprotein_dephosphorylation`, and 41fp OOS preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_41fp_1025.json`. EC 3.1.3.16/48
is scope only; counted corroboration comes from protein-phosphatase family/name context, dinuclear
metal/cofactor or binding-site context, and phosphoprotein dephosphorylation reaction evidence.

No rows were applied because live UniProt REST reads stalled before complete previews could be
written. Timeout-bounded preview windows across offsets 0-14 record **13** fetched candidate rows,
**0** target mechanism-corroborated rows, **13** `no_mechanism_corroboration` holds, **0**
novelty-admitted rows, and **26** fetch failures; blocker details are in
`work/ser_thr_protein_phosphatase_live_sourcing_blocker_current702_20260614.md`. Honest counters
therefore remain external registry **7308** rows, combined label surface **8010**, combined seed
surface **6314**, positive bronze **6267**, OOS bronze **1696**, silver_confirmed **47**, and
projected **0**.

Post-run local artifacts are current: high-yield factory reports **1** ready existing lane
(`ser_thr_protein_phosphatase`) with projected clean admits **150**; coverage reports no holes and
Gini **0.1807**; novelty replay remains **6847** admit / **414** throttle / **47** reject.
Bronze->silver preview now reports **202** silver-ready pending geometry rows, **1630**
chemistry-disagree holds, and **1779** low-cohesion holds; refreshed geometry confirmation found
**0** additional silver passes among **108** runnable rows. Next action is to rerun bounded Ser/Thr
previews under stable UniProt access, then row-audit/apply only if all mechanism-first gates pass.

**2026-06-14 automation update: alpha/beta hydrolase esterase/lipase lane applied and next lane reset.**
Treat this as the newest operational state. Registry-size safety remains green: the external
registry is still a small sharded manifest plus shard files below the per-file safety threshold.
Frozen current702 remained byte-unchanged at sha `5eec9bef...`.

The guarded alpha/beta hydrolase esterase/lipase lane now exists and has been applied:
`src/catalytic_earth/alpha_beta_hydrolase_esterase_lipase_sourcing.py`,
`scripts/source_alpha_beta_hydrolase_esterase_lipase_family.py`, new fingerprint
`alpha_beta_hydrolase_esterase_lipase`, ontology family `ser_his_acid_ester_hydrolysis`, and 40fp
OOS preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_40fp_1025.json`. EC 3.1.1 is
scope only; counted corroboration comes from non-EC family/domain context, Ser-His-Asp/Glu
active-site context, and Rhea ester-hydrolysis evidence. Protease/amidase, glycoside hydrolase,
transglycosylase, metal hydrolase, EC-only, and unresolved multi-fingerprint confounds remain held.

Applied result:
`artifacts/v3_alpha_beta_hydrolase_esterase_lipase_sourcing_preview_aggregate_current702_20260614.json`
admitted **150** rows after bounded-window aggregation, dedup/novelty/cap gates, and
`artifacts/v3_alpha_beta_hydrolase_esterase_lipase_row_guardrail_audit_current702_20260614_aggregate.json`
found **0** row-level guardrail problems. Current honest counters: external registry **7308** rows
= **6084** external seed labels + **1224** external OOS labels, with **30** external
silver-confirmed. Combined label surface **8010**; combined seed surface **6314**; combined OOS
**1696**; positive bronze **6267**; silver_confirmed **47** including the frozen 17; projected
**0**. Remaining seed gap to 10k is **3686**.

Post-apply coverage and novelty remain green: coverage reports no holes/under-floor fingerprints,
fingerprint Gini **0.1807**, and only `metal_dependent_hydrolase` over cap; novelty replay reports
**6847** admit / **414** throttle / **47** reject across **7308** external rows. The refreshed
high-yield factory finds no existing lane with >=150 cap room and selects
`ser_thr_protein_phosphatase` as the next new-fingerprint runner to build.

**2026-06-14 automation update: aldehyde dehydrogenase lane applied and next lane reset.** Treat
this as the newest operational state. Registry-size safety remains green: the external registry is
still a small sharded manifest plus shard files below the per-file safety threshold. Frozen
current702 remained byte-unchanged at sha `5eec9bef...`.

The guarded aldehyde dehydrogenase lane now exists and has been applied:
`src/catalytic_earth/aldehyde_dehydrogenase_sourcing.py`,
`scripts/source_aldehyde_dehydrogenase_family.py`, new fingerprint `aldehyde_dehydrogenase`,
ontology node `cys_thiohemiacetal_aldehyde_oxidation`, and 39fp OOS preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_39fp_1025.json`. EC 1.2.1 is
scope only; counted corroboration comes from non-EC mechanism axes such as ALDH family/domain,
NAD(P) cosubstrate or binding-site context, Rhea aldehyde oxidation, and catalytic Cys/Glu evidence
where available.

Applied result:
`artifacts/v3_aldehyde_dehydrogenase_sourcing_preview_current702_20260614.json` admitted **150**
rows after dedup/novelty/cap gates, and
`artifacts/v3_aldehyde_dehydrogenase_row_guardrail_audit_current702_20260614.json` found **0**
row-level guardrail problems. Current honest counters: external registry **7158** rows = **5934**
external seed labels + **1224** external OOS labels, with **30** external silver-confirmed.
Combined label surface **7860**; combined seed surface **6164**; combined OOS **1696**;
silver_confirmed **47** including the frozen 17; projected **0**. Remaining seed gap to 10k is
**3836**.

Post-apply coverage and novelty remain green: coverage reports no holes/under-floor fingerprints,
fingerprint Gini **0.1835**, and only `metal_dependent_hydrolase` over cap; novelty replay reports
**6702** admit / **409** throttle / **47** reject across **7158** external rows. The refreshed
high-yield factory finds no existing lane with >=150 cap room and selects
`alpha_beta_hydrolase_esterase_lipase` as the next new-fingerprint runner to build. The design-only
contract is
`artifacts/v3_alpha_beta_hydrolase_esterase_lipase_lane_preregistration_current702_20260614_post_aldehyde_dehydrogenase_apply.json`:
use esterase/lipase family/name context, Ser-His-Asp/Glu active-site or binding-site context, and
Rhea ester hydrolysis as non-EC corroborators; hold protease/amidase, glycoside hydrolase,
transglycosylase, metal hydrolase, EC-only, and unresolved multi-fingerprint confounds.

**2026-06-14 automation update: HAD-like phosphatase lane applied and next lane reset.** Treat this
as the newest operational state. Registry-size safety remains green: the external registry is still
a small sharded manifest plus four shards below the per-file safety threshold. Frozen current702
remained byte-unchanged at sha `5eec9bef...`.

The guarded HAD-like phosphatase lane now exists and has been applied:
`src/catalytic_earth/had_like_phosphatase_sourcing.py`,
`scripts/source_had_like_phosphatase_family.py`, new fingerprint `had_like_phosphatase`, ontology
node `had_aspartyl_phosphoenzyme_hydrolysis`, and 38fp OOS preregistration artifact
`artifacts/v3_external_hard_negative_next_tranche_preregistration_38fp_1025.json`. EC 3.1.3 is
scope only; counted corroboration comes from non-EC mechanism axes such as HAD family/domain,
Mg/Asp phosphoenzyme context, active/binding-site evidence, or Rhea phosphomonoester hydrolysis.

Applied result:
`artifacts/v3_had_like_phosphatase_sourcing_preview_current702_20260614.json` admitted **146**
rows after dedup/novelty/cap gates, and
`artifacts/v3_had_like_phosphatase_row_guardrail_audit_current702_20260614.json` found **0**
row-level guardrail problems. A broader 500-record probe saturated at **145** admits, so do not
rerun HAD as a mass-growth lane without a new evidence handle.

Current honest counters: external registry **7008** rows = **5754** external positive bronze +
**1224** external OOS bronze + **30** external silver-confirmed. Combined label surface **7710**;
combined seed surface **6014**; combined positive bronze **5967**; combined OOS bronze **1696**;
silver_confirmed **47** including the frozen 17; projected **0**. Remaining seed gap to 10k is
**3986**.

Post-apply coverage and novelty remain green: coverage reports no holes/under-floor fingerprints,
fingerprint Gini **0.1891**, and only `metal_dependent_hydrolase` over cap; novelty replay reports
**6552** admit / **409** throttle / **47** reject across **7008** external rows. The refreshed
high-yield factory finds no existing lane with >=150 cap room and selects
`aldehyde_dehydrogenase` as the next new-family runner to build with the same mechanism-first
guardrails. The design-only contract is now
`artifacts/v3_aldehyde_dehydrogenase_lane_preregistration_current702_20260614_post_had_apply.json`:
use ALDH family/name, NAD(P) cosubstrate or binding-site context, and catalytic Cys/Glu active-site
evidence as non-EC corroborators, and hold molybdopterin/flavin/generic NAD(P) aldehyde
oxidoreductase confounds.

**2026-06-14 automation update: first external silver confirmations applied by the separate
geometry gate.** Treat this as the newest operational state. The registry-size hard blocker remains
clear: the external registry is still a small sharded manifest plus four shards below the per-file
safety threshold. Frozen current702 remained byte-unchanged at sha `5eec9bef...`.

The separate geometry-confirmation lane now exists:
`src/catalytic_earth/silver_geometry_confirmation_run.py` and
`scripts/run_silver_geometry_confirmation.py`. It consumes only rows that already pass the
silver-runnability audit (recorded holo PDB confirmation, sha-matched local coordinate file, and
explicit PDB chain/residue mappings), builds local geometry features from the mmCIF file, and reuses
the existing geometry retrieval + label-factory promotion rule. It does not score from UniProt
binding-site prose/roles, EC, Rhea, names, or source text.

Applied result:
`artifacts/v3_silver_geometry_confirmation_run_current702_20260614_apply.json` scored **154**
runnable rows, promoted **30** to silver, and held **124**. Post-apply pending state is **230**
silver-ready rows: **124** runnable but held by the geometry gate and **106** still blocked before
geometry confirmation. `artifacts/v3_silver_geometry_confirmation_run_current702_20260614_post_apply_pending.json`
confirms **0** additional pass rows under the current gate. The preview/audit code now excludes
already silver-confirmed rows from the pending queue.

Current honest counters: external registry **6862** rows = **5608** external positive bronze +
**1224** external OOS bronze + **30** external silver-confirmed. Combined label surface remains
**7564**; combined seed surface remains **5868**; combined positive bronze **5821**; combined OOS
bronze **1696**; silver_confirmed **47** including the frozen 17; projected **0**. Continue silver
quality via explicit residue mapping for the 106 blockers and representation/calibration review for
the 124 runnable holds, but resume high-yield bronze growth in parallel while safety stays green.

Post-apply bounded follow-ups: the remaining UniProt PDB-ID preview queried **4842** missing-PDB
rows and found **0** new xrefs, so the current PDB-ID lane is exhausted without a new source or
no-xref policy. The refreshed bronze->silver preview reports **230** pending silver-ready rows,
**1344** chemistry-disagree rows, and **1759** low-cohesion holds. Cohesion calibration changed no
thresholds; **232** low-cohesion rows sit near the 0.92 threshold, but any family-specific
relaxation must be pre-registered and cannot be used to inflate counts. Coverage and novelty were
refreshed: fingerprint Gini **0.1891**, no floor holes, only `metal_dependent_hydrolase` over cap,
and novelty replay decisions **6406** admit / **409** throttle / **47** reject.

Next high-yield bronze action remains `had_like_phosphatase`. Use
`artifacts/v3_had_like_phosphatase_lane_preregistration_current702_20260614_post_silver_apply.json`
as the guardrail contract before creating the ontology node, fingerprint, source runner, and tests.
The fresh downstream eval design is recorded in `docs/fresh_leakage_safe_downstream_eval_design.md`
as design-only; do not treat it as an implemented or scored benchmark.

**2026-06-14 automation update: silver-ready queue partially materialized for real geometry
confirmation.** Treat this as the newest operational state. Registry file-size safety remains green:
the external registry is still a sharded manifest (~1.2 KB) plus four shards (largest ~17 MB), and
the new holo coordinate batch under `artifacts/v3_silver_holo_coordinates_current702/` totals ~243
MB with no file over 45 MB. External labels remain **6862** = positive bronze **5638** + OOS bronze
**1224**; combined label surface **7564**; combined seed-fingerprint surface **5868**; frozen
current702 sha remains `5eec9bef...`.

Silver quality advanced without changing tiers. The silver geometry audit is now sha-aware: local
coordinate files must match the recorded holo-confirmation sha. New bounded lanes materialized
sha-verified local holo PDB mmCIFs and mapped UniProt active-site positions to explicit PDB
chain/residue positions only through mmCIF alignment tables. Verified local holo-coordinate rows are
now **260**, clearing the local-coordinate blocker for the current silver-ready queue; explicit PDB
residue-mapped rows are **162**. Final audit
`artifacts/v3_silver_geometry_confirmation_audit_current702_20260614_post_fetch257_mapping.json`
found **154/260** silver-ready rows ready for the separate geometry-confirmation run, **106** still
blocked, and **0** silver flips. Remaining blockers: missing explicit PDB residue mapping **98** and
insufficient exact active-site residues **20**.

Next silver action is no longer a generic audit: run or implement the separate geometry-confirmation
gate for those **154** ready rows and apply silver only for rows that pass. Continue bounded
coordinate materialization + explicit mapping for the rest of the silver-ready queue in parallel
with high-yield bronze growth; do not let this quality lane permanently block the next
mechanism-first new-family runner.

**2026-06-14 automation update: silver geometry blocker audited, PDB-ID pool scaled, next growth
lane refreshed.** Treat this as the newest operational state. Registry file-size safety remains
green after the new writes: the external registry is still a sharded manifest (~1.2 KB) plus four
shards all below 18 MB. External labels remain **6862** = positive bronze **5638** + OOS bronze
**1224**; combined label surface **7564**; combined seed-fingerprint surface **5868**; remaining
seed gap **4132**; frozen current702 sha remains `5eec9bef...`.

PDB-ID backfill was advanced in bounded chunks. Rows with `evidence.structure_provenance.pdb_ids`
moved **1298 -> 2020** (+722 this run), with no row-count change and no predictive-evidence change.
The final 3000-row PDB probe backfilled **0** and mostly rechecked no-xref rows, so do not repeat
large PDB-ID chunks without improving the no-xref skip/recheck policy or changing the source.

The new silver geometry audit
`artifacts/v3_silver_geometry_confirmation_audit_current702_20260614.json` found **0/260** runnable
silver-ready rows and **0** silver flips. All 260 silver-ready rows lack explicit PDB chain/residue
mappings; 259 also lack a local holo coordinate file; 20 have insufficient exact active-site
residue evidence. This is now the concrete blocker for silver tier flips. UniProt sequence
positions are not valid PDB residue mappings; do not promote annotation-only or holo-only rows to
silver. Next silver action is a SIFTS/PDB residue-mapping + local holo-coordinate materialization
lane, then rerun the audit and only then run/apply the geometry gate.

Fresh non-mutating planning artifacts after this state:
`artifacts/v3_high_yield_family_lane_factory_current702_20260614_post_pdb_backfill.json` recommends
building `had_like_phosphatase` first (projected clean admits **150**; no existing lane has >=150
cap room), `artifacts/v3_breadth_feasibility_scout_current702_20260614_post_pdb_backfill.json`
projects reviewed Swiss-Prot clean-only positive bronze to **8509** (gap **1491**), and
`artifacts/v3_evidence_handle_expansion_current702_20260614_post_pdb_backfill.json` reports 4/6
handle-blocked families unlocked by better non-EC handles with reachable positive-bronze uplift
**741**. The external-surface eval split design artifact is design-only; no benchmark was run.

**2026-06-14 automation update: registry sharded, full suite green, bounded PDB-ID backfill
applied.** Treat this as the newest operational state. The external registry file-size blocker is
cleared: `data/registries/external_bronze_labels.json` is now a sharded-registry manifest
(**1203 bytes**) plus four shard files under `data/registries/external_bronze_labels.shards/`
(largest **17,996,716 bytes**). Loader/writer behavior is preserved through
`src/catalytic_earth/registry_io.py`.

Current honest counters after this safety run: external registry **6862** rows = positive bronze
**5638** + OOS bronze **1224**; combined label surface **7564**; combined seed-fingerprint surface
**5868**; remaining seed gap to 10k **4132**; silver-ready queue **260 pending geometry run**;
silver-confirmed tier count **17**. No tiers changed this run. Full suite from the actual final
state: **2238 passed, 1 warning, 244 subtests passed in 163.10s**.

New PDB-ID backfill infrastructure is available and was applied in a bounded chunk:
`scripts/backfill_label_pdb_ids.py --limit 120 --apply` copied UniProt `xref_pdb` provenance into
**19** external rows, raising rows with registry PDB IDs to **1298**. This is provenance only, not a
predictive feature; frozen current702 sha stayed `5eec9bef...`. A follow-up holo preview checked 50
rows and found **0** new holo confirmations, so do not claim new silver. Next safe actions are:
continue PDB-ID backfill in bounded chunks, rerun holo confirmation, and separately run the
authorized geometry-confirmation/tier-flip path for the existing 260 silver-ready queue. For bronze
growth, use the high-yield factory artifacts; do not return to exhausted copper or tiny cap topups.

**2026-06-14 automation update: protein kinase 37fp high-yield lane applied.** After the terpene
lane left only **77** cap slots, the latest run shifted to the next factory-supported high-yield
family rather than doing a tiny top-up. It added `protein_kinase_ser_thr_tyr` and
`protein_substrate_phosphoryl_transfer`, bumped the current positive universe to
`label_factory_v1_37fp`, registered deploy-missing context, and re-froze OOS preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_37fp_1025.json`.

Admission is mechanism-first: EC 2.7.10/2.7.11 scopes candidates only; counted corroboration must
come from non-EC protein-kinase family context, ATP/Mg cosubstrate context, and Rhea
protein-phosphoryl-transfer or active/binding-site evidence. EC, name, keyword, Rhea, ATP/Mg, and
site handles remain excluded-context source/admission evidence, never predictive features, and EC
is never a counted corroborator. Histidine kinases, small-molecule kinases, ATP ligases,
hydrolases, side-EC rows, EC-only rows, and multi-fingerprint rows stay held.

The first preview admitted **72** rows and was not applied. The enlarged audited preview
`artifacts/v3_protein_kinase_sourcing_preview470_current702_20260614.json` fetched **470**,
mechanism-corroborated **248**, held **0** off-target rows, novelty-admitted **150**, and held
**0** at cap. Row audit found **0** problems. Applied rows: external bronze **7213 -> 7363**
(+150), combined label surface **7915 -> 8065**, and `protein_kinase_ser_thr_tyr` **0 -> 150**,
exactly at its chemistry-confusable cap **150**. Combined seed-fingerprint surface is now
**6369**, leaving **3631** to 10k by that convention. Honest counters remain separate:
**positive_bronze_count 6352**, **oos_bronze_count 1696**, **silver_ready_count 0**,
**silver_confirmed_count 17**, **projected_provisional_count 0**.

Do not continue protein kinase under the current cap policy. The newest useful next step is to
rerun the high-yield factory against the 37fp applied state, then wire another high-yield new
family. Prefer `aldehyde_dehydrogenase` or `alpha_beta_hydrolase_esterase_lipase` for cleaner
boundaries, or `had_like_phosphatase` only if it is guarded against the existing over-cap
`metal_dependent_hydrolase`. Keep SDR/AKR blocked until they have source-free, non-EC mechanism
rules that separate them from capped NAD(P) dehydrogenase and neighboring redox families.

**2026-06-14 automation update: terpene cyclase/synthase 36fp high-yield lane applied.** The
latest run built the top-ranked factory lane instead of replaying capped/tiny top-ups. It added
`terpene_cyclase_synthase` plus `terpene_carbocation_cyclization`, bumped the current positive
universe to `label_factory_v1_36fp`, and re-froze OOS preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_36fp_1025.json`.

Admission is mechanism-first: reviewed EC 4.2.3 scopes candidates only; non-EC terpene/cyclase
family context plus Mg/Mn or diphosphate context and Rhea/site evidence must corroborate. EC,
keyword, Rhea, metal, and diphosphate handles remain excluded-context source/admission evidence,
never predictive features, and EC is never a counted corroborator. Prenyltransferase
chain-extension, generic hydratase/lyase, side-EC, EC-only, and multi-fingerprint rows stay held.

The first narrow preview admitted **112** rows and was not applied. The broader preview
`artifacts/v3_terpene_cyclase_synthase_broad250_sourcing_preview_current702_20260614.json` fetched
**416**, mechanism-corroborated **188**, held **48** off-target rows, held **134** no-corroboration
rows, novelty-admitted **173**, and held **0** at cap. Row audit found **0** problems. Applied rows:
external bronze **7040 -> 7213** (+173), combined label surface **7742 -> 7915**,
`terpene_cyclase_synthase` **0 -> 173** under cap **250**. Combined seed-fingerprint surface is now
**6219**, leaving **3781** to 10k by that convention. Honest counters remain separate:
**positive_bronze_count 6202**, **oos_bronze_count 1696**, **silver_ready_count 0**,
**silver_confirmed_count 17**, **projected_provisional_count 0**.

Do not continue terpene as the next high-yield lane under the current objective: remaining cap room
is **77**, below the >=150 batch gate. Next high-yield work should wire another new family through
the same 36fp->37fp OOS preregistration, disambiguation, source-runner, preview, row-audit, and
apply gates. The leading candidate is `short_chain_dehydrogenase_reductase` only if the SDR rule
can separate it from capped `nad_p_dehydrogenase`, AKR/MDR, and flavin/metal redox boundaries.

**2026-06-14 automation update: high-yield family scout + reusable lane factory built.** The
latest run stopped replaying capped/tiny lanes and checked whether any existing fingerprint/source
path could still admit a >=150 clean batch. Current evidence says no: remaining existing cap rooms
are below threshold or source-exhausted. Therefore no registry apply was attempted.

A refreshed reviewed-UniProt supply scout
`artifacts/v3_high_yield_family_supply_scout_current702_20260614.json` probed **18** candidate
families and found **14** clean/floor-reachable candidates under broad cap math, but projected only
**8687** positive bronze from reviewed Swiss-Prot alone (gap **1313** to 10k even before applying
newer current-count/cap-room constraints). The new factory artifact
`artifacts/v3_high_yield_family_lane_factory_current702_20260614.json` then ranked **12** concrete
family-lane specs against current counts and live non-EC corroborator-reachable supply. It found
**0** existing lanes ready for >=150 and **8** blocked high-yield new-family lanes. Top ranked:
`terpene_cyclase_synthase`, with reviewed scope supply **2335**, non-EC corroborator supply
**2315**, estimated corroboration rate **0.991**, clean cap **250**, and projected clean admits
**250**.

Reusable infrastructure added: `src/catalytic_earth/high_yield_family_lane_factory.py`,
`scripts/build_high_yield_family_lane_factory.py`, and
`tests/test_high_yield_family_lane_factory.py`. The factory declarations include scope query,
non-EC corroborator query, disambiguation holds, cap class, source tier, rationale, row guardrail
requirement, and preview/apply command templates. Guardrails remain unchanged: EC is scope-only and
never a counted corroborator; broadened handles are admission/source-planning evidence only;
future labels must be bronze, automation-curated, `uniprot:*`, deduped against current702 and
external bronze, novelty-gated, capped, and written only to the external bronze registry after
explicit `--apply`.

Counts are unchanged by this run: external bronze **7040**, combined label surface **7742**,
combined seed-fingerprint surface **6046**, remaining gap to 10k seed surface **3954**. Frozen
current702 stayed sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Next 10k-path work should
build the `terpene_cyclase_synthase` fingerprint/source runner first: ontology node,
OOS/fingerprint-universe preregistration, mechanism disambiguation rule, source runner,
row-guardrail audit, non-destructive preview, targeted tests, then `--apply` only if all gates pass.

**2026-06-14 automation update: Stage-1 radical-SAM post-prefix top-up applied.** Current handoff
evidence showed the previously obvious continuation lanes were capped or exhausted: non-heme 2OG is
**250/250**, current copper selectors have no post-prefix supply, SOD's guarded query had already
fetched its full **252** reviewed rows, and zinc post-apply previews were redundant/no-yield. The
run therefore used the existing Stage-1 cofactor pipeline for remaining non-confusable cofactor
surface.

The run added fetch-only row windows to the Stage-1 source runner:
`--record-offset-per-lane` and `--record-limit-per-lane`. These controls are applied before
entry/Rhea fetch and do not change EC scope, mechanism corroboration, trust tiers, novelty, caps, or
predictive evidence. The Stage-1 `--apply` path now prints frozen current702 sha256 before and
after append.

Applied rows: the radical/cobalamin post-prefix slice
`--holes radical_sam_enzyme cobalamin_radical_rearrangement --max-records-per-lane 180
--record-offset-per-lane 100 --record-limit-per-lane 40` fetched **160**, disambiguated **82**, and
applied **81** `radical_sam_enzyme` source-tier-0 bronze rows. One off-target `coa_acyltransferase`
row was held at cap; `cobalamin_radical_rearrangement` remained **144**. `radical_sam_enzyme` moved
**133 -> 214** combined, below cap **250**.

External bronze is now **7040**; combined label surface is **7742**. External-only split is
**5816** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is **6046**,
leaving **3954** to 10k by that surface convention. The strict counter ledger remains separate:
**positive_bronze_count 6029**, **oos_bronze_count 1696**, **silver_ready_count 0**,
**silver_confirmed_count 17**, **projected_provisional_count 0**. Frozen current702 stayed
byte-unchanged with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`;
growth went only to `data/registries/external_bronze_labels.json`.

Fresh audits: row guardrail audit over the **81** newly applied rows found **0** problems. Coverage
audit reports **35** fingerprints, Gini **0.1385**, holes `[]`, under-floor `[]`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **0**. Novelty replay over
**7040** expansion rows reports decisions `{'admit': 6584, 'reject': 47, 'throttle': 409}` and
would-not-readmit **456** (0.0648). Follow-on FMO/heme Stage-1 windows `0:30` and `30:30` fetched
**125** and **107** rows respectively but final-admitted **0** after novelty/cap gates; do not apply
those previews. Next work may cautiously preview `radical_sam_enzyme` at `140:40` while cap room
remains (**214/250**), or scout a clean under-cap family/source path with explicit non-EC
mechanism corroborators.

**2026-06-13/14 automation update: non-heme iron 2OG capped; copper post-prefix scout
no-yield.** The latest run continued the documented non-heme 2OG window sequence from offset 140
and applied six more bounded windows: `140:10` (+6), `150:10` (+5), `160:10` (+5), `170:10`
(+3), `180:10` (+4), and `190:10` (+4). Net movement was **223 -> 250** (+27), exactly at the
non-confusable cap **250**. The final window held one otherwise gate-admitted row at cap. Do not
continue `non_heme_iron_2og_dioxygenase` under current cap policy.

External bronze is now **6959**; combined label surface is **7661**. External-only split is
**5735** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is
**5965**, leaving **4035** to 10k by that surface convention. The strict counter ledger remains
separate: **positive_bronze_count 5948**, **oos_bronze_count 1696**, **silver_ready_count 0**,
**silver_confirmed_count 17**, **projected_provisional_count 0**. Frozen current702 stayed
byte-unchanged with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`;
growth went only to `data/registries/external_bronze_labels.json`.

Fresh audits: row guardrail audit over all **250** non-heme 2OG rows found **0** problems.
Coverage audit reports **35** fingerprints, Gini **0.137**, holes `[]`, under-floor `[]`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **0**. Novelty replay over
**6959** expansion rows reports decisions `{'admit': 6503, 'reject': 47, 'throttle': 409}` and
would-not-readmit **456** (0.0655).

Continuation work added fetch-only source-window controls to the copper oxidoreductase runner and
proved the current two copper selectors are exhausted beyond the previously fetched prefix:
`--max-records-per-lane 320 --record-offset-per-lane 240 --record-limit-per-lane 40` fetched
**0** rows, with lane totals **153** laccase/oxidase rows and **69** amine oxidase rows.
`copper_oxidoreductase` remains **140/250**, but do not replay the current copper lanes. Next work
should scout alternate copper source handles with explicit non-EC mechanism corroborators, or pick
a clean source-supply scout/spec for another under-cap family rather than padding capped lanes.

**2026-06-13 automation update: non-heme iron 2OG windowed extension applied.** After all former
floor lanes were closed and capped, the run used an existing under-cap, mechanism-first family lane
instead of relaxing admission. It added source-fetch-only window controls to the non-heme 2OG
runner (`--record-offset-per-lane` and `--record-limit-per-lane`) and applied six bounded windows
for `non_heme_iron_2og_dioxygenase`: `80:10` (+17), `90:10` (+13), `100:10` (+15), `110:10`
(+3), `120:10` (+2), and `130:10` (+1). Net movement was **172 -> 223** (+51) under the
non-confusable cap **250**.

External bronze is now **6932**; combined label surface is **7634**. External-only split is
**5708** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is
**5938**, leaving **4062** to 10k by that surface convention. The strict counter ledger remains
separate: **positive_bronze_count 5921**, **oos_bronze_count 1696**, **silver_ready_count 0**,
**silver_confirmed_count 17**, **projected_provisional_count 0**. Frozen current702 stayed
byte-unchanged with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`;
growth went only to `data/registries/external_bronze_labels.json`.

Fresh audits: row guardrail audit over all **223** non-heme 2OG rows found **0** problems.
Coverage audit reports **35** fingerprints, Gini **0.135**, holes `[]`, under-floor `[]`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **0**. Novelty replay over
**6932** expansion rows reports decisions `{'admit': 6476, 'reject': 47, 'throttle': 409}` and
would-not-readmit **456** (0.0658). The final windows tapered in yield; next continuation, if any,
should preview `--record-offset-per-lane 140 --record-limit-per-lane 10` and apply only if the same
novelty/trust-tier/cap/leakage gates pass. Otherwise choose a clean new family/source scout.

**2026-06-13 automation update: tier-2 PfkB/biotin/glycoside floors closed and capped.** The
latest run added a source-trust tier parameter to the existing cofactor/EC disambiguation path and
opt-in unreviewed UniProt tier-2 lanes for `glycoside_hydrolase`,
`biotin_dependent_carboxylase`, and `pfkb_ribokinase_family`. Defaults remain `source_tier_0`.
The unreviewed lanes require `--source-tier source_tier_2`, and tier 2 uses the existing
`source_trust_tiers.evaluate_corroboration` three-axis mechanism gate. EC/name/Rhea/keyword/prose/
feature handles remain excluded-context admission evidence only; EC is never counted; and
`predictive_evidence []`.

Bounded applies added **236** bronze rows through the existing mechanism-first path:
`glycoside_hydrolase` **84 -> 150** (+66), `biotin_dependent_carboxylase` **84 -> 150** (+66), and
`pfkb_ribokinase_family` **46 -> 150** (+104). PfkB and biotin gained `--record-offset-per-lane`
and `--record-limit-per-lane` source-window controls after the first applies; these are fetch-only
controls and do not alter admission, trust tiers, novelty, caps, or predictive evidence. All three
former floor families are now exactly at their chemistry-confusable **150/150** caps and should not
continue under current cap policy.

External bronze is now **6881**; combined label surface is **7583**. External-only split is
**5657** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is
**5887**, leaving **4113** to 10k by that surface convention. The strict counter ledger remains
separate: **positive_bronze_count 5870**, **oos_bronze_count 1696**, **silver_ready_count 0**,
**silver_confirmed_count 17**, **projected_provisional_count 0**. Frozen current702 stayed
byte-unchanged with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`;
growth went only to `data/registries/external_bronze_labels.json`.

Fresh audits: row guardrail audit over all **236** tier-2 rows found **0** problems. Coverage audit
reports **35** fingerprints, Gini **0.1312**, holes `[]`, under-floor `[]`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **0**. Novelty replay over
**6881** expansion rows reports decisions `{'admit': 6425, 'reject': 47, 'throttle': 409}` and
would-not-readmit **456** (0.0663).

Next work: do **not** continue PfkB, biotin, glycoside, CoA, P450, molybdopterin, racemase,
isomerase, or other capped lanes without a cap-policy change or a real new chemistry split with
OOS preregistration if the fingerprint universe changes. The next 10k-path lane should be a clean
new family/source scout or spec with non-EC mechanism corroborators.

**2026-06-13 automation update: windowed CoA/P450/molybdopterin cap-fills applied.** The latest
run added `--record-offset-per-lane` / `--record-limit-per-lane` source-window controls to
`scripts/source_coa_acyltransferase_family.py`, `scripts/source_cytochrome_p450_family.py`, and
`scripts/source_molybdopterin_oxidoreductase_family.py`. This was a source-fetch-only change; it
does not alter admission, trust-tier, novelty, caps, or predictive evidence.

Windowed applies added **107** bronze rows through the existing mechanism-first path:
`molybdopterin_oxidoreductase` **207 -> 250** (+43), `cytochrome_p450_monooxygenase`
**248 -> 250** (+2), and `coa_acyltransferase` **188 -> 250** (+62). All three are now **250/250**
and should not continue under the current cap policy. Frozen current702 stayed byte-unchanged with
sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
`data/registries/external_bronze_labels.json`.

External bronze is now **6645**; combined label surface is **7347**. External-only split is
**5421** seed-fingerprint rows and **1224** OOS rows. Combined seed-fingerprint surface is
**5651**, leaving **4349** to 10k by that surface convention. The strict counter ledger remains
separate: **positive_bronze_count 5634**, **oos_bronze_count 1696**, **silver_ready_count 0**,
**silver_confirmed_count 17**, **projected_provisional_count 0**. Coverage audit reports **35**
fingerprints, Gini **0.1704**, holes `[]`, under-floor
`['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **86**. Novelty replay over
**6645** expansion rows reports decisions `{'admit': 6189, 'reject': 47, 'throttle': 409}` and
would-not-readmit **456** (0.0686). Row audit found **0** problems across all **750** CoA/P450/
molybdopterin rows.

Next work: remaining floors are PfkB **46/100**, biotin **84/100**, and glycoside hydrolase
**84/100**. Do not continue CoA, P450, molybdopterin, racemase, isomerase, or other capped lanes
without a cap-policy change or a real new chemistry split. Prefer a genuinely new non-EC
corroborator/source path for the remaining floors, or scout/spec a clean new family not already
capped. EC/name/Rhea/keyword/prose/feature handles remain excluded-context admission evidence only,
EC is never counted, and `predictive_evidence []`.

**2026-06-13 automation update: isomerase cap-fill applied after glycoside alternate scouts
no-yielded.** The latest run first stayed on the under-floor path. A base glycoside hydrolase
page-2 continuation over rows **581-660**
(`scripts/source_glycoside_hydrolase_family.py --query-pages-per-lane 2 --record-offset-per-lane 580 --record-limit-per-lane 80`)
fetched **80**, mechanism-corroborated/admitted **0**, held **57** no-corroboration rows, skipped
**23**, and recorded **1** Rhea HTTP 500 (`Q59675`). The run then added
`--only-alternate-name-lanes` to the glycoside source runner as a source-fetch-only control so the
alternate chitinase/beta-glucanase/glycoside-hydrolase name lane can be scouted without refetching
the base lane. The first untried alternate-only window (`--record-offset-per-lane 40
--record-limit-per-lane 80`) fetched **80**, mechanism-corroborated/admitted **0**, and held
**80** no-corroboration rows. These are no-apply artifacts.

With under-floor source paths still no-yield/source-limited and substantial time remaining, the
run used the previously documented smallest under-cap retry:
`scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --apply`.
It fetched **405**, target mechanism-corroborated **91**, novelty gate admitted **80** before the
cap guard, applied **8**, held@cap **72**, novelty-throttled/rejected **11**, held **61** off-target
`nad_p_dehydrogenase` rows, held **90** no-corroboration rows, skipped **163**, and recorded **0**
fetch failures on the apply rerun. Frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
`data/registries/external_bronze_labels.json`.

External bronze is now **6538**; combined label surface is **7240**;
`cofactor_independent_isomerase` is **150/150** and should not be continued under the current
chemistry-confusable cap. External-only bronze split is **5314** seed-fingerprint rows and
**1224** OOS rows. Combined seed-fingerprint label surface is **5544**, leaving **4456** to 10k by
that surface convention. The strict source-trust counter ledger remains separate:
**positive_bronze_count 5527**, **oos_bronze_count 1696**, **silver_ready_count 0**,
**silver_confirmed_count 17**, **projected_provisional_count 0**. Coverage audit reports
**35** fingerprints, fingerprint Gini **0.1611**, holes `[]`, under-floor
`['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **86**. Novelty replay over
**6538** expansion rows reports decisions `{'admit': 6082, 'reject': 47, 'throttle': 409}` and
would-not-readmit **456** (0.0697). Row audit found **0** problems across all **150** isomerase
rows.

Next work: remaining floors are PfkB **46/100**, biotin **84/100**, and glycoside hydrolase
**84/100**. Build a genuinely new non-EC corroborator/source path for those floors, or scout/spec a
clean new family not already at cap. EC/name/Rhea/keyword/prose/feature handles remain
excluded-context admission evidence only, EC is never counted, and `predictive_evidence []`.

**2026-06-13 automation update: racemase window400:80 reached cap; strict kinase source-supply
scout scaffolded.** The latest run applied the next bounded non-PLP metal racemase/epimerase
window only after prior under-floor PfkB/biotin/glycoside source paths were documented
source-limited/no-yield under mechanism-first gates. Apply:
`scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 500 --record-offset-per-lane 400 --record-limit-per-lane 80 --cap-ceiling 150 --apply`.
It fetched **80**, mechanism-corroborated **34**, novelty gate admitted **28** before the cap
guard, applied **21**, held@cap **7**, novelty-throttled/rejected **6**, held **23** off-target
`nad_p_dehydrogenase` rows, held **22** no-corroboration rows, skipped **1**, and recorded **0**
fetch failures. Frozen current702 stayed byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
`data/registries/external_bronze_labels.json`.

External bronze is now **6530**; combined label surface is **7232**;
`metal_racemase_epimerase_non_plp` is now **150/150** and should not be continued under the current
chemistry-confusable cap. External-only bronze split is **5306** seed-fingerprint rows and
**1224** OOS rows. Combined seed-fingerprint label surface is **5536**, leaving **4464** to 10k by
that surface convention. The strict source-trust counter ledger remains separate:
**positive_bronze_count 5519**, **oos_bronze_count 1696**, **silver_ready_count 0**,
**silver_confirmed_count 17**, **projected_provisional_count 0**. Coverage audit reports
**35** fingerprints, fingerprint Gini **0.1619**, holes `[]`, under-floor
`['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **86**. Novelty replay over
**6530** expansion rows reports decisions `{'admit': 6074, 'reject': 47, 'throttle': 409}` and
would-not-readmit **456** (0.0698). Row audit found **0** problems across all **150** racemase
rows.

Continuation work after the apply did not force another cap-fill lane. A bounded strict-kinase
entry/Rhea scout over hexokinase/glucokinase, glycerol kinase, and
galactokinase/mevalonate/homoserine blocked before artifact write in UniProt entry TLS handshake,
so a blocker artifact was written. A cheaper source-supply TSV scout then sampled **60** rows with
**0** fetch failures and **0** generated labels. It ranks
`galactokinase_mevalonate_homoserine` first by reviewed supply (**613** total), but the first
20-row window was only **1/20 registry-new**; this is not enough to wire a fingerprint. Next work:
remaining floors are PfkB **46/100**, biotin **84/100**, and glycoside hydrolase **84/100**. Build
a genuinely new non-EC corroborator/source path for those floors, or run a deeper windowed strict
kinase source scout plus a small entry/Rhea mechanism scout before any fingerprint/ontology/OOS
prereg work. EC/name/Rhea/keyword/prose/feature handles remain excluded-context admission evidence
only, EC is never counted, and `predictive_evidence []`.

**2026-06-13 automation update: racemase windowed top-up applied after under-floor scouts
no-yielded.** The latest run respected the remaining-floor priority before cap-fill work. A new
biotin alternate floor-closure source flag
(`scripts/source_biotin_dependent_carboxylase_family.py --include-alternate-floor-closure-lanes`)
tested Rhea/raw-EC selectors from the prior PfkB/biotin scout and produced **0** admissible rows
from **139** fetched candidates because the registry-new rows lacked non-EC mechanism
corroboration. A new glycoside alternate-name source flag
(`scripts/source_glycoside_hydrolase_family.py --include-alternate-name-lanes`) searched EC 3.2.1
chitinase/beta-glucanase/glycoside-hydrolase names using already-recognized family-text handles;
the bounded 40-row window fetched **80** across two lanes and admitted **0**. Zinc hydratase
cap-fill fetched **160**, found **3** target mechanism-corroborated rows, and admitted **0** because
all 3 were novelty-throttled as redundant. These previews are durable no-apply artifacts, not label
growth.

The productive continuation was a non-PLP metal racemase/epimerase cap-fill. A monolithic 500-row
top-up blocked before artifact write in live UniProt entry fetch, so the run added
`--record-offset-per-lane` and `--record-limit-per-lane` to the racemase source runner and processed
the unspent **320:80** search-row window. Apply:
`scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 500 --record-offset-per-lane 320 --record-limit-per-lane 80 --cap-ceiling 150 --apply`.
It fetched **80**, mechanism-corroborated **21**, applied **21**, held **49** off-target
`nad_p_dehydrogenase` rows, held **10** no-corroboration rows, skipped **0**, novelty-throttled
**0**, held@cap **0**, and kept frozen current702 byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

External bronze is now **6509**; combined label surface is **7211**; honest counters stay separate:
**positive_bronze 5515**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
**projected 0**. External-only bronze split is **5285** seed-fingerprint rows and **1224** OOS rows.
Remaining positive-bronze gap to 10k: **4485**. `metal_racemase_epimerase_non_plp` is **129/150**.
Coverage audit reports **35** fingerprints, fingerprint Gini **0.1643**, holes `[]`, under-floor
`['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **86**. Novelty replay over
**6509** expansion rows reports decisions `{'admit': 6053, 'reject': 47, 'throttle': 409}` and
would-not-readmit **456** (0.0701). Guardrails remain active: EC/name/Rhea/keyword/prose/feature
handles are excluded-context admission evidence only, EC is never counted, and
`predictive_evidence []`. Next work should still prefer genuinely new non-EC corroborator/source
paths for PfkB **46/100**, biotin **84/100**, or glycoside hydrolase **84/100**; if no such path is
ready, the racemase cap-fill can continue with the next bounded window **400:80** only after cap and
novelty gates are inspected.

**2026-06-13 automation update: glycoside hydrolase floor-window applied and paging support
added.** The latest run continued `glycoside_hydrolase` as an under-floor 35fp family. To avoid
repeating the previous no-artifact monolithic 500-row fetch, the run added row-window support to
the shared external ingestion pilot and exposed glycoside CLI flags
`--record-offset-per-lane`, `--record-limit-per-lane`, and `--query-pages-per-lane`. These flags
only decide which reviewed UniProt search rows are entry/Rhea-fetched; they do not alter admission,
trust-tier, dedup, novelty, cap, or leakage rules.

The applied window used rows **421-500** from the guarded reviewed EC 3.2.1 glycoside query:
`scripts/source_glycoside_hydrolase_family.py --max-records-per-lane 500 --record-offset-per-lane 420 --record-limit-per-lane 80 --cap-ceiling 150 --apply`.
It fetched **80**, mechanism-corroborated **14**, applied **12**, held **66** no-corroboration rows,
skipped **0**, off-target held **0**, novelty-throttled **2**, held@cap **0**, and had **0** fetch
failures on the apply rerun. Frozen current702 remained byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
`data/registries/external_bronze_labels.json`.

External bronze is now **6488**; combined label surface is **7190**; `glycoside_hydrolase` is
**84/150** and still below the 100 floor. Honest counters stay separate: **positive_bronze 5494**,
**oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**, **projected 0**.
External-only bronze split is **5264** seed-fingerprint rows and **1224** OOS rows. Remaining
positive-bronze gap to 10k: **4506**. Post-apply coverage audit reports **35** fingerprints,
fingerprint Gini **0.1675**, holes `[]`, under-floor
`['pfkb_ribokinase_family', 'biotin_dependent_carboxylase', 'glycoside_hydrolase']`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **86**. Novelty replay over
**6488** expansion rows reports decisions `{'admit': 6032, 'reject': 47, 'throttle': 409}` and
would-not-readmit **456** (0.0703). Row audit found **0** problems across all **84** glycoside
hydrolase rows.

Guardrails remain active: EC/name/Rhea/keyword/prose/feature handles are admission/excluded-context
evidence only; EC is never counted; `predictive_evidence []`; glycosyltransferase,
transglycosylase, phosphorylase, lyase, side-EC, EC-only, and multi-fingerprint-signal rows are
held. A second-page preview using `--query-pages-per-lane 2 --record-offset-per-lane 500
--record-limit-per-lane 80` fetched **80** but mechanism-corroborated/admitted **0**. Do not repeat
the applied `420:80` window or apply the zero-yield `500:80` page-2 artifact. Remaining floors are
PfkB **46/100**, biotin **84/100**, and glycoside hydrolase **84/100**; next work should build a
genuinely new strict PfkB/biotin source/corroborator path or an alternate glycoside source lane with
non-EC mechanism corroboration.

**2026-06-13 automation update: glycoside hydrolase top-up applied; floor still open.** The latest
run continued the under-floor `glycoside_hydrolase` lane through the existing 35fp
mechanism-first pipeline. The 420-row top-up
(`scripts/source_glycoside_hydrolase_family.py --max-records-per-lane 420 --cap-ceiling 150 --apply`)
fetched **420**, mechanism-corroborated **27**, applied **27**, held **290**
no-corroboration rows, skipped **103**, held **0** off-target rows, novelty-throttled **0**,
held@cap **0**, and had **0** fetch failures. Frozen current702 remained byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; growth went only to
`data/registries/external_bronze_labels.json`.

External bronze is now **6476**; combined label surface is **7178**; `glycoside_hydrolase` is
**72/150** and still below the 100 floor. Honest counters stay separate: **positive_bronze 5482**,
**oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**, **projected 0**.
External-only bronze split is **5252** seed-fingerprint rows and **1224** OOS rows. Remaining
positive-bronze gap to 10k: **4518**. Post-apply coverage audit reports **35** fingerprints,
fingerprint Gini **0.1699**, holes `[]`, under-floor
`['biotin_dependent_carboxylase', 'glycoside_hydrolase', 'pfkb_ribokinase_family']`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **98**. Novelty replay over
**6476** expansion rows reports decisions `{'admit': 6020, 'reject': 47, 'throttle': 409}` and
would-not-readmit **456** (0.0704). Row audit found **0** problems across all **72** glycoside
hydrolase rows.

Guardrails remain active: EC/name/Rhea/keyword/prose/feature handles are admission/excluded-context
evidence only; EC is never counted; `predictive_evidence []`; glycosyltransferase,
transglycosylase, phosphorylase, lyase, side-EC, EC-only, and multi-fingerprint-signal rows are
held. A follow-on `--max-records-per-lane 650` attempt was rejected by the runner cap of 500; a
500-row preview was stopped for closeout before artifact write while in UniProt entry TLS/connect
work. Next concrete work should retry the 500-row glycoside preview early in a run, or add
paging/resume support before deeper windows. Remaining floors are PfkB **46/100**, glycoside
hydrolase **72/100**, and biotin **84/100**.

**2026-06-13 automation update: glycoside hydrolase 35fp bronze lane applied.** The run chose a
new clean 10k-path family after PfkB/biotin remained source-limited and a GHKL histidine-kinase
scout found only **1** likely wireable reviewed row. A glycoside hydrolase scout over **240**
reviewed EC 3.2.1 rows found **194** registry-new rows and **178** likely wireable by non-EC
mechanism handles. The family was completed through the full pipeline: added
`glycoside_hydrolase` fingerprint, `glycosidic_bond_hydrolysis` ontology node, deploy-missing
context `glycosidic_substrate_ordered_water_hydrolysis_context`, coverage source signature,
`label_factory_v1_35fp`, OOS preregistration
`artifacts/v3_external_hard_negative_next_tranche_preregistration_35fp_1025.json`,
disambiguation/trust-tier/leakage/coverage tests, non-destructive preview, and explicit `--apply`
with frozen current702 sha checks. Frozen current702 remained byte-unchanged with sha256
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Production apply
(`scripts/source_glycoside_hydrolase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`)
fetched **240**, mechanism-corroborated **45**, applied **45**, held **155** no-corroboration rows,
skipped **40**, off-target held **0**, novelty-throttled **0**, held@cap **0**, and recorded **1**
Rhea timeout (`P19531`). Glycoside hydrolase is now **45/150** and remains below the 100 floor.

External bronze is now **6449**; combined label surface is **7151**; honest counters stay separate:
**positive_bronze 5438**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
**projected 0**. External-only bronze split is **5225** seed-fingerprint rows and **1224** OOS rows.
Remaining positive-bronze gap to 10k: **4562**. Post-apply coverage audit reports **35**
fingerprints, fingerprint Gini **0.1753**, holes `[]`, under-floor
`['biotin_dependent_carboxylase', 'glycoside_hydrolase', 'pfkb_ribokinase_family']`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **125**. Novelty replay over
**6449** expansion rows reports decisions `{'admit': 5993, 'reject': 47, 'throttle': 409}` and
would-not-readmit **456** (0.0707). Row audit found **0** problems across **45** glycoside
hydrolase rows.

Guardrails remain active: EC/name/Rhea/keyword/prose/feature handles are admission/excluded-context
evidence only; EC is never counted; `predictive_evidence []`; glycosyltransferase,
transglycosylase, phosphorylase, lyase, side-EC, EC-only, and multi-fingerprint-signal rows are
held. Next concrete work should close the remaining floors through gated top-up/new-source work:
glycoside hydrolase **45/100**, PfkB **46/100**, or biotin **84/100**. Do not repeat the weak GHKL
scout as a production lane.

**2026-06-13 automation update: Mn/Fe SOD 34fp bronze expansion applied.** The spec-only
`manganese_iron_superoxide_dismutase` lane from the latest handoff was completed through the full
mechanism-first pipeline. The run added the fingerprint and `metal_superoxide_dismutation` ontology
node, bumped the universe to `label_factory_v1_34fp`, re-froze OOS preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_34fp_1025.json`, added
disambiguation/trust-tier/leakage/source tests, ran non-destructive previews, and applied only
after dedup/novelty/governor/cap/trust-tier gates passed. Frozen current702 remained byte-unchanged
with sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Initial apply
(`scripts/source_manganese_iron_superoxide_dismutase_family.py --max-records-per-lane 240 --cap-ceiling 250 --apply`)
fetched **240**, mechanism-corroborated **181**, applied **164**, held **59** no-corroboration rows,
novelty-throttled **17**, and held **0** off-target/cap rows. A bounded top-up
(`--max-records-per-lane 320 --cap-ceiling 250 --apply`) fetched **252**, skipped **164**
already-existing rows, mechanism-corroborated **19**, applied **2**, held **69** no-corroboration
rows, novelty-throttled **17**, and held **0** off-target/cap rows. SOD is now **166/250** and
above floor.

External bronze is now **6404**; combined label surface is **7106**; honest counters stay separate:
**positive_bronze 5393**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
**projected 0**. External-only bronze split is **5180** seed-fingerprint rows and **1224** OOS rows.
Remaining positive-bronze gap to 10k: **4607**. Post-apply coverage audit reports **34**
fingerprints, fingerprint Gini **0.1608**, holes `[]`, under-floor
`['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, only `metal_dependent_hydrolase`
over-cap, and next-batch floor deficit **70**. Novelty replay over **6404** expansion rows reports
decisions `{'admit': 5948, 'reject': 47, 'throttle': 409}` and would-not-readmit **456** (0.0712).
Row audit found **0** problems across **166** SOD rows.

Guardrails remain active: EC/name/Rhea/keyword/prose/feature handles are admission/excluded-context
evidence only; EC is never counted; `predictive_evidence []`; Cu/Zn SOD, heme/peroxidase/
cytoglobin/hemoglobin, nitrite/nitric-oxygen dioxygenase, superoxide reductase, side-EC, EC-only,
and multi-fingerprint-signal rows are held. Next concrete work should not repeat the exhausted SOD
first-window or top-up previews. Build a genuinely new strict source/corroborator path for
PfkB **46/100** or biotin **84/100**, or scout/spec the next clean fingerprint family through the
same gated pipeline.

**2026-06-13 automation update: Mn/Fe SOD source blocker cleared and 34fp next-lane spec
written.** After bounded under-cap previews admitted 0 rows, this run did not repeat those same
first-window probes. A PfkB/biotin alternate-source scout found limited registry-new reviewed
supply and boundary-heavy rows, so the run switched to a cleaner new-family scout. The previous
breadth-feasibility row had classified `manganese_iron_superoxide_dismutase` as source-poor because
the count query required `cc_cofactor:manganese/iron`; a guarded EC/name/cofactor query now finds
**252** reviewed Mn/Fe SOD rows:
`(reviewed:true) AND (ec:1.15.1.1) AND ((cc_cofactor:manganese) OR (cc_cofactor:iron) OR
(protein_name:manganese) OR (protein_name:iron) OR (protein_name:Mn) OR (protein_name:Fe)) NOT
((cc_cofactor:copper) OR (cc_cofactor:zinc) OR (protein_name:"Cu-Zn") OR (protein_name:"Cu/Zn") OR
(protein_name:copper) OR (protein_name:zinc))`.

The non-destructive mechanism scout sampled **80** rows with **0** fetch failures: **80/80**
registry-new, **80/80** RHEA:20696/superoxide dismutation context, **80/80** Mn/Fe metal context,
**80/80** SOD family text, **77/80** active/binding/metal-site evidence, and **0** explicit
Cu/Zn/heme/side-EC boundary flags. No labels were generated and no registry write was performed.
Artifacts:
`artifacts/v3_pfkb_biotin_alternate_source_scout_current702_20260613.json`,
`work/pfkb_biotin_alternate_source_scout_current702_20260613.md`,
`artifacts/v3_manganese_iron_superoxide_dismutase_source_mechanism_scout_current702_20260613.json`,
`work/manganese_iron_superoxide_dismutase_source_mechanism_scout_current702_20260613.md`,
`artifacts/v3_manganese_iron_superoxide_dismutase_next_lane_spec_current702_20260613.json`, and
`work/manganese_iron_superoxide_dismutase_next_lane_spec_current702_20260613.md`.

Counts remain external bronze **6238**, combined label surface **6940**, and frozen current702
**702** with sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest
counters stay separate: **positive_bronze 5227**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**. Next exact action: wire
`manganese_iron_superoxide_dismutase` as a deliberate `label_factory_v1_34fp` fingerprint through
the full pipeline. Required implementation: fingerprint + `metal_superoxide_dismutation` ontology
node, deploy-missing context `mn_fe_superoxide_redox_dismutation_context`, OOS prereg re-freeze,
disambiguation/trust-tier/leakage tests, non-destructive preview, then `--apply` only if novelty,
dedup, governor, cap, and trust-tier gates pass. Required guards: hold Cu/Zn SOD, heme/cytoglobin/
hemoglobin/peroxidase/nitrite/nitric-oxygen dioxygenase, superoxide reductase, side-EC, EC-only,
and multi-fingerprint-signal rows.

**2026-06-13 automation update: bounded under-cap previews cleared the fetch blocker but admitted
0 rows.** A follow-up run isolated the previous live-fetch blocker. The sourcing runners complete
and write artifacts at small `--max-records-per-lane`; the previous no-artifact behavior was caused
by larger sequential UniProt entry/Rhea evidence-fetch workloads before artifact write, not by a
broken gate. Bounded first-window previews were run for approved under-cap lanes:
`cofactor_independent_isomerase` 5 rows/lane (14 fetched, 0 mechanism, 0 admitted) and 20 rows/lane
(67 / 0 / 0), `coa_acyltransferase` 20 rows/lane (75 / 0 / 0),
`non_heme_iron_2og_dioxygenase` 20 rows/lane (66 / 3 / 0; all novelty-throttled as redundant),
`molybdopterin_oxidoreductase` 20 rows/lane (67 / 2 / 0; throttled), `zinc_lyase_hydratase`
20 rows/lane (20 / 0 / 0), and `copper_oxidoreductase` 20 rows/lane (40 / 1 / 0; throttled).
No `--apply` was run.

Counts remain external bronze **6238**, combined label surface **6940**, and frozen current702
**702** with sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest
counters stay separate: **positive_bronze 5227**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**. Aggregate artifact/report:
`artifacts/v3_under_cap_bounded_preview_no_yield_current702_20260613.json` and
`work/under_cap_bounded_preview_no_yield_current702_20260613.md`.

Next concrete work should not repeat these same bounded first-window probes. Either design a new
PfkB/biotin source path with stronger mechanism corroboration, run a targeted deeper under-cap probe
only when enough time remains for preview completion/validation/push/lock release, or start a
new-family mechanism/source-supply scout/spec if evidence is cleaner than further top-ups.

**2026-06-13 automation update: under-cap extension previews blocked by live fetch latency.** The
latest handoff still leaves `pfkb_ribokinase_family` **46/100** and
`biotin_dependent_carboxylase` **84/100** under floor, but their current strict reviewed source
paths are exhausted under the mechanism-first gate. This run therefore attempted already approved
under-cap extension/cap-fill previews instead of relaxing EC scope: CoA/acyl-CoA acyltransferase
(**188/250**) at 500 and 280 rows/lane, then cofactor-independent isomerase (**142/150**) at
120 rows/lane. The live fetch/evidence-extraction attempts did not produce preview artifacts quickly
enough for a safe inspect/apply/validate cycle; no `--apply` was run and no labels changed.

Counts remain external bronze **6238**, combined label surface **6940**, and frozen current702
**702** with sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest
counters stay separate: **positive_bronze 5227**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**. Blocker artifacts:
`artifacts/v3_under_cap_extension_live_fetch_blocker_current702_20260613.json` and
`work/under_cap_extension_live_fetch_blocker_current702_20260613.md`.

Next exact action: retry the smallest cap-fill first:
`PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --out artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json --report work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md`.
Apply only if the preview produces inspectable rows and `floor_projection`, `novelty_gate`,
held@cap, source-trust tier, namespace/tier/review-status, `predictive_evidence`, and
excluded-context/leakage fields pass. Do not add more P450 without explicit new reaction/organism
justification because it is **248/250**; do not broad-wire EC-only kinase rows or force
source-limited PfkB/biotin deficits.

**2026-06-13 automation update: P450 and copper extension applies are now completed.** The latest
handoff left two under-floor lanes, `pfkb_ribokinase_family` and `biotin_dependent_carboxylase`,
but both strict reviewed source paths are exhausted under current gates. This run therefore used
two already approved, non-confusable extension lanes with remaining reviewed supply while keeping
the same mechanism-first admission pipeline and cap governor.

P450 extension
(`scripts/source_cytochrome_p450_family.py --max-records-per-lane 240 --cap-ceiling 250 --out artifacts/v3_cytochrome_p450_extension_sourcing_preview_current702_20260613.json --report work/cytochrome_p450_extension_sourcing_current702_20260613.md`)
fetched **337**, mechanism-corroborated **189**, applied **138**, held **35** no-corroboration
rows, skipped **113** already-covered/current-registry rows, novelty-throttled **51**, and moved
`cytochrome_p450_monooxygenase` **110 -> 248** under cap 250. Copper extension
(`scripts/source_copper_oxidoreductase_family.py --max-records-per-lane 240 --cap-ceiling 250 --out artifacts/v3_copper_oxidoreductase_extension_sourcing_preview_current702_20260613.json --report work/copper_oxidoreductase_extension_sourcing_current702_20260613.md`)
fetched **222**, mechanism-corroborated **81**, applied **21**, held **20** no-corroboration rows,
skipped **121**, novelty-throttled **60**, and moved `copper_oxidoreductase` **119 -> 140**.

External bronze is now **6238**; combined label surface is **6940**; frozen current702 remains
**702** with sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest
counters stay separate: **positive_bronze 5227**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**. External-only bronze split is 5014 seed-fingerprint rows
and 1224 OOS rows. Remaining positive-bronze gap to 10k: **4773**. Post-apply audit:
**33 fingerprints**, fingerprint Gini **0.1633**, holes `[]`, under-floor
`['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, only `metal_dependent_hydrolase`
over-cap, next-batch floor deficit **70**. Novelty replay: **6238** expansion rows, decisions
`{'admit': 5782, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0731). Row audits
found **0** problems across all 138 P450 rows and 21 copper rows.

All added rows keep `predictive_evidence []`; EC/name/keyword/Rhea/prose/feature handles remain
excluded-context admission evidence and are never predictive; EC is never counted. Do **not** add
more P450 without explicit new reaction/organism justification because P450 is **248/250**. PfkB
remains **46/100** and biotin **84/100**; the next concrete work should find genuinely new strict
PfkB/biotin source paths with stronger corroboration, or scout/spec a new fingerprint family if
evidence is cleaner than further balanced-lane top-ups.

**2026-06-13 automation update: strict PfkB/ribokinase-family 33fp expansion is now applied.**
The post-PfkA handoff left `pfkb_ribokinase_family` as a guarded candidate, and this run completed
a strict mechanism-first 33fp lane after tightening the PfkB/PfkA boundary. Added
`pfkb_ribokinase_family` fingerprint + `pfkb` ontology mapping, bumped to
`label_factory_v1_33fp`, and re-froze OOS preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_33fp_1025.json`. EC 2.7.1 is
scope-only, chemistry-confusable, capped at 150, and separated from broad EC 2.7 plus NDK/dNK/ASKHA/
GHMP/PfkA kinase subclasses. Generic `fructokinase` is not counted as PfkB family evidence because
it shadowed PfkA `6-phosphofructokinase`.

PfkB apply
(`scripts/source_pfkb_ribokinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`)
fetched **88**, mechanism-corroborated **46**, applied **46**, held **36** no-corroboration rows,
skipped **2**, off-target held **4** as `askha_sugar_acetate_kinase`, throttled **0**, and held
**0** at cap. External bronze is now **6079**; combined label surface is **6781**; frozen current702
remains **702** with sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
Honest counters stay separate: **positive_bronze 5085**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. External-only bronze split is 4855
seed-fingerprint rows and 1224 OOS rows. Remaining positive-bronze gap to 10k: **4915**.
Post-apply audit: **33 fingerprints**, fingerprint Gini **0.162**, holes `[]`, under-floor
`['biotin_dependent_carboxylase', 'pfkb_ribokinase_family']`, only `metal_dependent_hydrolase`
over-cap, next-batch floor deficit **70**. Novelty replay: **6079** expansion rows, decisions
`{'admit': 5623, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.075). Row audit
`artifacts/v3_pfkb_ribokinase_family_row_guardrail_audit_current702_20260613.json` found **0**
problems across all 46 PfkB rows and all four mechanism axes present on every row.

All added rows keep `predictive_evidence []`; EC/name/keyword/Rhea/prose/feature handles remain
excluded-context admission evidence and are never predictive. Counted corroboration comes from
ATP/ADP phosphoryl-transfer Rhea participant text with PfkB/ribokinase acceptors,
PfkB/ribokinase-family text, ATP/Mg/substrate active-/binding-site evidence,
cofactor/cosubstrate handles, and structure-compatible evidence. Do **not** broad-wire EC 2.7 or
merge kinase subclasses. A follow-on floor-extension scout
`artifacts/v3_pfkb_ribokinase_family_floor_extension_scout_current702_20260613.json` reran the
strict reviewed lane with `--max-records-per-lane 500` and found **0** new PfkB labels (48 skipped
as already covered, 36 no-corroboration holds, 4 off-target ASKHA rows), so the current reviewed
PfkB query is exhausted at **46/100**. The next concrete work should close under-floor positives by
returning to the biotin **16**-row deficit, designing a genuinely new PfkB source/handle path with
stronger corroboration, or selecting a new 10k-path family through the full gated pipeline.

**2026-06-13 automation update: strict PfkA phosphofructokinase 32fp expansion is now applied.**
The post-dNK scout selected strict `pfka_phosphofructokinase`, and this run completed that full
pipeline. Added `pfka_phosphofructokinase` fingerprint + existing `pfka` ontology mapping, bumped
to `label_factory_v1_32fp`, and re-froze OOS preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_32fp_1025.json`. EC 2.7.1 is
scope-only, chemistry-confusable, capped at 150, and separated from broad EC 2.7 plus NDK/dNK/ASKHA/
GHMP/PfkB kinase subclasses.

PfkA apply
(`scripts/source_pfka_phosphofructokinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`)
fetched **240**, mechanism-corroborated **233**, applied **150**, held **5** no-corroboration rows,
skipped **2**, held **83** at cap, and held **0** off-target rows. External bronze is now **6033**;
combined label surface is **6735**; frozen current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters stay
separate: **positive_bronze 5039**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k: **4961**.
Post-apply audit: **32 fingerprints**, fingerprint Gini **0.1465**, holes `[]`, under-floor
`['biotin_dependent_carboxylase']`, only `metal_dependent_hydrolase` over-cap, next-batch floor
deficit **16**. Novelty replay: **6033** expansion rows, decisions
`{'admit': 5577, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0756). Row audit
`artifacts/v3_pfka_phosphofructokinase_row_guardrail_audit_current702_20260613.json` found **0**
problems across all 150 PfkA rows and all four mechanism axes present on every row.

All added rows keep `predictive_evidence []`; EC/name/keyword/Rhea/prose/feature handles remain
excluded-context admission evidence and are never predictive. Counted corroboration comes from
ATP/ADP phosphoryl-transfer Rhea participant text with fructose-6-phosphate, PfkA/ATP-dependent
6-phosphofructokinase family text, ATP/Mg/substrate active-/binding-site evidence,
cofactor/cosubstrate handles, and structure-compatible evidence. Do **not** broad-wire EC 2.7 or
merge kinase subclasses. The next durable artifact
`work/pfkb_ribokinase_family_next_lane_spec_current702_20260613.md` records PfkB as a guarded
candidate only: reviewed supply **85**, sampled **28/40** likely wireable, and active-/binding-site
context only **28/40**. Tighten/re-scout PfkB before any 33fp pipeline, or choose a stronger
current scaling-plan family if evidence is cleaner.

**2026-06-13 automation update: strict deoxynucleoside kinase 31fp expansion is now applied.** The
post-ASKHA/GHMP handoff selected strict `deoxynucleoside_kinase`, and this run completed that full
pipeline. Added `deoxynucleoside_kinase` fingerprint + existing `dnk` ontology mapping, bumped to
`label_factory_v1_31fp`, and re-froze OOS preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_31fp_1025.json`. EC 2.7.1 is
scope-only, chemistry-confusable, capped at 150, and separated from broad EC 2.7 and the NDK/ASKHA/
GHMP/Pfk subclasses.

dNK apply
(`scripts/source_deoxynucleoside_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`)
fetched **240**, mechanism-corroborated **237**, applied **150**, held **87** at cap, and held
**0** off-target rows. External bronze is now **5883**; combined label surface is **6585**; frozen
current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters stay
separate: **positive_bronze 4889**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k: **5111**.
Post-apply audit: **31 fingerprints**, fingerprint Gini **0.1534**, holes `[]`, under-floor
`['biotin_dependent_carboxylase']`, only `metal_dependent_hydrolase` over-cap, next-batch floor
deficit **16**. Novelty replay: **5883** expansion rows, decisions
`{'admit': 5427, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0775). Row audit
`artifacts/v3_deoxynucleoside_kinase_row_guardrail_audit_current702_20260613.json` found **0**
problems across all 150 dNK rows and all four mechanism axes present on every row.

All added rows keep `predictive_evidence []`; EC/name/keyword/Rhea/prose/feature handles remain
excluded-context admission evidence and are never predictive. Counted corroboration comes from
ATP/ADP phosphoryl-transfer Rhea participant text with deoxynucleoside substrates, dNK family text,
ATP/substrate active-/binding-site evidence, cofactor/cosubstrate handles, and structure-compatible
evidence. Do **not** broad-wire EC 2.7 or merge kinase subclasses. Follow-on scout
`artifacts/v3_strict_kinase_subclass_source_scout_after_dnk_current702_20260613.json` generated
**0** labels and wrote no registry; it found strict `pfka_phosphofructokinase` reviewed supply
**386** with **40/40** sampled likely wireable and **0/40** sampled boundary signals, versus
`pfkb_ribokinase_family` **85** reviewed supply with **28/40** sampled likely wireable. The next
concrete lane is strict `pfka_phosphofructokinase`: fingerprint + ontology node -> 32fp OOS prereg
re-freeze -> disambiguation guards/tests -> non-destructive preview -> gated apply only if
novelty/governor/dedup/trust-tier/leakage gates pass.

**2026-06-13 automation update: strict ASKHA 29fp and GHMP 30fp kinase-subclass expansions are now
applied.** The post-NDK scout selected strict `askha_sugar_acetate_kinase`, and this run continued
to strict `ghmp_small_molecule_kinase` after ASKHA because time remained and the reviewed source
supply was clean enough. Both lanes are EC 2.7.1 scope-only, chemistry-confusable, capped at 150,
and separated from broad EC 2.7. Added `askha_sugar_acetate_kinase` fingerprint + `askha` ontology
node, bumped to `label_factory_v1_29fp`, and re-froze OOS preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_29fp_1025.json`. Added
`ghmp_small_molecule_kinase` fingerprint + `ghmp` ontology node, bumped to `label_factory_v1_30fp`,
and re-froze OOS preregistration as
`artifacts/v3_external_hard_negative_next_tranche_preregistration_30fp_1025.json`.

ASKHA apply
(`scripts/source_askha_sugar_acetate_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`)
fetched **240**, mechanism-corroborated **227**, applied **150**, held **9** no-corroboration rows,
throttled **7**, held **70** at cap, and held **0** off-target rows. GHMP apply
(`scripts/source_ghmp_small_molecule_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`)
fetched **240**, mechanism-corroborated **228**, applied **150**, held **10** no-corroboration rows,
throttled **0**, held **78** at cap, and held **0** off-target rows. External bronze is now
**5733**; combined label surface is **6435**; frozen current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters stay
separate: **positive_bronze 4739**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k: **5261**.
Post-apply audit: **30 fingerprints**, fingerprint Gini **0.1534**, holes `[]`, under-floor
`['biotin_dependent_carboxylase']`, only `metal_dependent_hydrolase` over-cap, next-batch floor
deficit **16**. Novelty replay: **5733** expansion rows, decisions
`{'admit': 5277, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0795).

All added rows keep `predictive_evidence []`; EC/name/keyword/Rhea/prose/feature handles remain
excluded-context admission evidence and are never predictive. Counted corroboration comes from
ATP/ADP phosphoryl-transfer Rhea participant text, family/domain text, ATP/Mg or substrate
active-/binding-site evidence, cofactor/cosubstrate handles, and structure-compatible evidence.
Do **not** broad-wire EC 2.7 or merge kinase subclasses. The next concrete lane is strict
`deoxynucleoside_kinase`, scaffolded in
`work/deoxynucleoside_kinase_next_lane_spec_current702_20260613.md`: reviewed supply **278**,
sampled **39/40** likely wireable, **1/40** boundary signal. Required next path is fingerprint +
`dnk` ontology node -> 31fp OOS prereg re-freeze -> disambiguation guards/tests -> non-destructive
preview -> gated apply only if novelty/governor/dedup/trust-tier/leakage gates pass.

**2026-06-13 automation update: biotin floor closure partially applied; strict NDK 28fp expansion is
now applied.** The latest handoff required a biotin floor-closure scout first. A new optional
Rhea-first lane for ATP/hydrogencarbonate carboxylation reactions found only **3** additional safe
biotin rows under the existing mechanism-first gate. `biotin_dependent_carboxylase` is now **84/100**
and remains under floor by **16**; do not relax the carboxylation requirement or admit EC 6.3.4.15
biotin-protein ligase rows to force closure.

The fallback narrow kinase-subclass path split strict `nucleoside_diphosphate_kinase` from broad
EC 2.7. The broad EC 2.7 lane remains blocked by subclass mixing. Strict NDK excludes protein kinase
EC 2.7.11, two-component histidine kinase EC 2.7.13, hydrolase/nuclease EC 3.*, and adenylate/
guanylate/NMP kinase side ECs. Added `nucleoside_diphosphate_kinase` fingerprint +
`phosphohistidine_ntp_transfer` ontology family, bumped
`CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_28fp`, and re-froze OOS
preregistration as `artifacts/v3_external_hard_negative_next_tranche_preregistration_28fp_1025.json`.
EC 2.7.4.6 is scope-only; counted handles are Rhea NTP/NDP phosphoryl-transfer participant text,
NDK family text, active-site phosphohistidine/catalytic-His or binding-site evidence, and structure.
Live apply
(`scripts/source_nucleoside_diphosphate_kinase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`)
fetched **240**, mechanism-corroborated **238**, gate-admitted **237**, applied **150**, held@cap
**87**, novelty-throttled **1**, off-target held **0**, duplicate skipped **0**. External bronze is
now **5433**; combined label surface is **6135**; frozen current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters stay separate:
**positive_bronze 4439**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
**projected 0**. Remaining positive-bronze gap to 10k: **5561**. Post-apply audit: **28
fingerprints**, fingerprint Gini **0.1608**, holes `[]`, under-floor
`['biotin_dependent_carboxylase']`, only `metal_dependent_hydrolase` over-cap, next-batch floor
deficit **16**. Novelty replay: **5433** expansion rows, decisions
`{'admit': 4977, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0839). All added rows
keep `predictive_evidence []`; EC/name/keyword/Rhea/prose/feature handles remain excluded-context
admission evidence and are never predictive. Next useful action: continue strict kinase-subclass
scouts/splits such as `deoxynucleoside_kinase`, `ghmp_small_molecule_kinase`, or
`askha_sugar_acetate_kinase`; do **not** broad-wire EC 2.7.

Follow-on scout artifact
`artifacts/v3_strict_kinase_subclass_source_scout_after_ndk_current702_20260613.json` sampled those
strict kinase splits without generating labels. Reviewed supply / likely wireable sample / sampled
boundary signal: `deoxynucleoside_kinase` **278 / 39-of-40 / 1**,
`ghmp_small_molecule_kinase` **613 / 37-of-40 / 0**, and
`askha_sugar_acetate_kinase` **667 / 39-of-40 / 0**. Prefer strict
`askha_sugar_acetate_kinase` for the next full 29fp pipeline; GHMP and deoxynucleoside kinase are
backups. Do not merge kinase subclasses or count EC as mechanism evidence.

**2026-06-13 automation update: biotin-dependent carboxylase 27fp expansion is now applied but
under floor.** The latest handoff blocked broad EC 2.7 kinase wiring and recommended either a
narrow kinase subclass or a guarded biotin-carboxylase handle. This run followed the biotin lane
because ATP/hydrogencarbonate/carboxybiotin Rhea chemistry plus biotin/biotinyl-Lys evidence is a
clean mechanism-first handle. Added `biotin_dependent_carboxylase` fingerprint +
`biotin_carboxyl_transfer` ontology family, bumped
`CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_27fp`, and re-froze OOS
preregistration as `artifacts/v3_external_hard_negative_next_tranche_preregistration_27fp_1025.json`.
EC 6.4.1 / 6.3.4 is scope-only; counted mechanism handles are biotin or biotinyl-Lys cofactor/
modified-residue evidence, Rhea ATP/hydrogencarbonate/carboxybiotin participant text, carboxylase
family text, active-/binding-site evidence, or structure. Kinase/phosphotransferase, hydrolase,
transferase side EC, non-scope side EC, PLP/ThDP/Mo/heme/flavin, multi-fingerprint signals, and
EC 6.3.4.15 biotin-protein ligase rows are held.

Live apply
(`scripts/source_biotin_dependent_carboxylase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`)
fetched **126**. An initial 93-row apply exposed 12 EC 6.3.4.15 biotin-protein ligase boundary rows;
the gate was corrected to require ATP-dependent carboxylation chemistry, and those rows were removed
from both the registry append and preview artifact. Corrected result: mechanism-corroborated/
admitted/applied **81**, disambiguation holds **44**, off-target held **0**, novelty-throttled/
rejected **0**, skipped **1**, held at cap **0**. External bronze is now **5280**; combined label
surface is **5982**; frozen current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters stay
separate: **positive_bronze 4269**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k: **5731**.
Post-apply audit: **27 fingerprints**, fingerprint Gini **0.1655**, holes `[]`, under-floor
`['biotin_dependent_carboxylase']`, only `metal_dependent_hydrolase` over-cap, next-batch floor
deficit **19**. Novelty replay: **5280** expansion rows, decisions
`{'admit': 4824, 'reject': 47, 'throttle': 409}`, would-not-readmit **456** (0.0864). All added
rows keep `predictive_evidence []`; EC/name/keyword/Rhea/prose handles remain excluded-context
admission evidence and are never predictive. Next useful action: run a non-destructive biotin
floor-closure source scout for the remaining **19** rows while keeping ATP + hydrogencarbonate/CO2/
carboxybiotin chemistry mandatory; if reviewed source supply cannot close the deficit, leave biotin
under floor and return to a narrow kinase-subclass scout. Do **not** broad-wire EC 2.7.

**2026-06-13 automation update: zinc lyase/hydratase 26fp expansion is now applied.** The latest
handoff explicitly recommended `zinc_lyase_hydratase` after the ThDP apply. The guarded lane added
`zinc_lyase_hydratase` fingerprint + `zinc_hydro_lyase` ontology family, bumped
`CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION` to `label_factory_v1_26fp`, and re-froze OOS
preregistration as `artifacts/v3_external_hard_negative_next_tranche_preregistration_26fp_1025.json`.
EC 4.2.1 is scope-only; counted mechanism handles are Zn cofactor/site evidence, Rhea hydration/
dehydration/carbonic reaction context, Lyase/hydratase family text, active-/binding-/metal-site
evidence, or structure. PLP, ThDP, hydrolase/transferase/aldolase/isomerase side rows,
non-4.2.1 side ECs, and multi-fingerprint signals are held. Live apply
(`scripts/source_zinc_lyase_hydratase_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`)
fetched **240**, mechanism-corroborated **116**, admitted/applied **113**, held **57** off-target
fingerprint matches (`nad_p_dehydrogenase` 47, `metallophosphomonoesterase` 6,
`metallo_amidohydrolase_deaminase` 4), held **10** no-corroboration rows, novelty-throttled **3**,
and skipped **0** duplicates. External bronze is now **5199**; combined label surface is **5901**;
frozen current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest counters stay separate:
**positive_bronze 4188**, **oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**,
**projected 0**. Remaining positive-bronze gap to 10k: **5812**. Post-apply audit: **26
fingerprints**, fingerprint Gini **0.1559**, holes `[]`, only `metal_dependent_hydrolase` over-cap,
next-batch floor deficit **0**. All added rows keep `predictive_evidence []`; EC/name/keyword/Rhea/
prose handles remain excluded-context admission evidence and are never predictive. The broad EC 2.7
kinase lane remains blocked by its mechanism scout; with ThDP and zinc applied, remaining
post-class-II candidates are weaker (`enolase_superfamily_lyase` reaction-poor, biotin
carboxylase below floor under current handles, Mn/Fe SOD not floor-reachable). Next useful action:
run a focused scout that either splits a narrow kinase subclass with clean non-EC handles or designs
a guarded biotin-carboxylase handle around biotinyl-Lys/Rhea ATP-hydrogencarbonate evidence.

**2026-06-13 automation update: ThDP enzyme 25fp expansion is now applied.** The broad EC 2.7
kinase lane remains blocked by its own mechanism scout, so this run followed the next cleaner
fallback from the post-class-II ranking: `thiamine_diphosphate_enzyme`. A focused mechanism scout
(`artifacts/v3_thiamine_diphosphate_mechanism_handle_scout_current702_20260613.json`) examined
**80** reviewed UniProt entries with **0** fetch failures and found ThDP context **80/80**, Rhea
cross-reference **80/80**, Mg context **77/80**, active/binding-site context **73/80**, Rhea
carbonyl/decarboxylation/transfer text **62/80**, and likely wireable rows **65/80**; flavin,
side-EC, and kinase/hydrolase boundary signals required explicit guards. The lane was wired as a
deliberate 25-fingerprint universe change: `thiamine_diphosphate_enzyme` fingerprint +
`thiamine_diphosphate_ylide` ontology family, EC 2.2.1/4.1.1/1.2.4 scope-only rule, ThDP/Mg, Rhea
decarboxylation/carbonyl-transfer/ThDP participant, ThDP-family keyword/domain, and active-/
binding-site corroborators, PLP/molybdopterin/flavin/heme/kinase/hydrolase/side-EC/multi-signal
guards, 25fp OOS preregistration re-freeze, offline leakage/trust-tier tests, non-destructive
preview, then explicit apply. Live apply
(`scripts/source_thiamine_diphosphate_family.py --max-records-per-lane 240 --cap-ceiling 150 --apply`)
fetched **240**, mechanism-corroborated **181**, admitted/applied **150**, held **14** off-target
`coa_acyltransferase` rows, held **37** no-corroboration rows, and skipped **0** duplicates.
External bronze is now **5086**; combined label surface is **5788**; frozen current702 remains
**702** with sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`. Honest
counters stay separate: **positive_bronze 4075**, **oos_bronze 1696**, **silver_ready 0**,
**silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k: **5925**.
Post-apply audit: **25 fingerprints**, fingerprint Gini **0.1541**, holes `[]`, only
`metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. All added rows keep
`predictive_evidence []`; EC/name/keyword/Rhea/prose handles remain excluded-context admission
evidence and are never predictive. Follow-on mechanism scout
`artifacts/v3_zinc_lyase_hydratase_mechanism_handle_scout_current702_20260613.json` found
`zinc_lyase_hydratase` is the next viable unapplied lane (zinc context **80/80**, Rhea hydration/
elimination/carbonic text **79/80**, active/binding/metal site **76/80**, likely wireable **50/80**),
but side-EC/boundary rows **30/80** mean the next run must wire explicit guards before any 26fp
preview/apply.

**2026-06-13 automation update: ATP amide ligase 23fp and class-II metal aldolase 24fp expansions
are now applied.** The prompt's older P450 instruction was superseded by the current handoff:
P450, non-heme 2OG, CoA, cofactor-independent isomerase, molybdopterin, copper, and non-PLP
racemase/epimerase were already applied. This run followed the latest lane evidence. First,
`atp_amide_ligase` was wired with EC 6.3 as scope-only and ATP/ADP/phosphate/Mg, Ligase/ATP-grasp
keyword/domain, Rhea amide/C-N/acyl-phosphate chemistry, or active-/binding-site mechanism
corroborators; biotin/carboxylase, kinase/phosphotransferase, hydrolase/transferase side rows, and
multi-signal rows are held. It applied **150** bronze rows
(`artifacts/v3_atp_amide_ligase_sourcing_preview_current702.json`), taking external bronze
**4636 -> 4786** and combined surface **5338 -> 5488**. A post-ATP source-supply scout then selected
`class_ii_metal_aldolase` as the next clean reviewed-Swiss-Prot lane
(`artifacts/v3_next_lane_source_supply_scout_after_atp_ligase_current702_20260613.json`). Its
mechanism scout (`artifacts/v3_class_ii_metal_aldolase_mechanism_handle_scout_current702_20260613.json`)
examined **80** entries with **0** fetch failures and found active/binding/metal site **80/80**,
metal **80/80**, Lyase **80/80**, Rhea **80/80**, aldolase/oxoacid **61/80**, and C-C reaction text
**58/80**, plus boundary signals requiring PLP/ThDP/Schiff-class-I/hydrolase/transferase/
oxidoreductase/side-EC guards. The lane was wired as a deliberate 24-fingerprint universe change:
`class_ii_metal_aldolase` fingerprint + `carbon_carbon_lyase` ontology family, EC 4.1.2/4.1.3
scope-only rule, metal/Lyase/aldolase/C-C/Rhea/active-site corroborators, 24fp OOS preregistration
re-freeze, offline leakage/trust-tier tests, non-destructive preview, then explicit apply. Live
apply (`scripts/source_class_ii_metal_aldolase_family.py --max-records-per-lane 240 --cap-ceiling
150 --apply`) fetched **240**, mechanism-corroborated **182**, admitted/applied **150**, and held
**7** off-target rows. External bronze is now **4936**; combined label surface is **5638**; frozen
current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after both applies.
Honest counters stay separate: **positive_bronze 3925**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k:
**6075**. Post-apply audit: **24 fingerprints**, fingerprint Gini **0.1581**, holes `[]`, only
`metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. All added rows keep
`predictive_evidence []`; EC/name/keyword/Rhea/prose handles remain excluded-context admission
evidence and are never predictive. Follow-on source-supply scout
`artifacts/v3_next_lane_source_supply_scout_after_class_ii_aldolase_current702_20260613.json` ranked
`atp_phosphotransferase_kinase` first, but the mechanism scout
`artifacts/v3_atp_phosphotransferase_kinase_mechanism_handle_scout_current702_20260613.json` blocks a
broad EC 2.7 25fp lane for now: ATP/ADP/phosphate, kinase text, and Rhea were present in **80/80**,
but multi-subclass boundary rows were **75/80** and only **4** rows were likely wireable without a
subclass split. Next recommended action: split a narrow kinase subclass with clean non-EC handles, or
choose the next cleaner lane from the scout ranking; **ThDP enzyme** is the best fallback candidate.

**2026-06-13 automation update: copper oxidoreductase 21fp and non-PLP racemase/epimerase 22fp
expansions are now applied.** The prompt's older P450 instruction was superseded by the current
handoff: P450, non-heme 2OG, CoA, cofactor-independent isomerase, and molybdopterin were already
applied. This run followed the latest lane evidence. First, `copper_oxidoreductase` was wired with
EC 1.10.3/1.4.3 as scope-only and copper cofactor/site, Rhea oxygen/redox, Copper keyword/domain, or
active-/binding-/metal-site mechanism corroborators; heme/flavin/molybdopterin/hydrolase/
non-oxidoreductase guards hold boundary rows. It applied **119** bronze rows
(`artifacts/v3_copper_oxidoreductase_sourcing_preview_current702.json`), taking external bronze
**4409 -> 4528** and combined surface **5111 -> 5230**. A post-copper source-supply scout then
selected `metal_racemase_epimerase_non_plp` as the next clean reviewed-Swiss-Prot lane
(`artifacts/v3_next_lane_source_supply_scout_after_copper_current702_20260613.json`): reviewed
supply **2141**, EC-only ceiling **2319**, distinct full EC sample **52**, clean/non-reaction-poor,
chemistry-confusable cap **150**. Its mechanism scout
(`artifacts/v3_metal_racemase_epimerase_mechanism_handle_scout_current702_20260613.json`) examined
**80** entries with **0** fetch failures and found Isomerase keyword **80/80**, Rhea
cross-reference **80/80**, isomerization reaction text **80/80**, racemase/epimerase text **78/80**,
binding-site **70/80**, active-site **59/80**, metal context **26/80**, cofactorless context
**42/80**, and PLP boundary **2/80**. The lane was wired as a deliberate 22-fingerprint universe
change: `metal_racemase_epimerase_non_plp` fingerprint + `stereochemical_isomerization` ontology
family, EC 5.1 scope-only rule, racemase/epimerase/mutarotase text, Rhea isomerization/racemization,
Isomerase keyword/domain, active-/binding-site, metal, or cofactorless admission handles, PLP and
side-EC guards, 22fp OOS preregistration re-freeze, offline leakage/trust-tier tests,
non-destructive preview, then explicit apply. Live apply
(`scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 320 --cap-ceiling 150 --apply`)
fetched **320**, mechanism-corroborated **108**, admitted/applied **108**, held **133** off-target
`nad_p_dehydrogenase` rows, held **48** no-corroboration rows, skipped **31**, and held **0** at cap.
External bronze is now **4636**; combined label surface is **5338**; frozen current702 remains
**702** with sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after
both applies. Honest counters stay separate: **positive_bronze 3625**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k:
**6375**. Post-apply audit: **22 fingerprints**, fingerprint Gini **0.1665**, holes `[]`, only
`metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. All added rows keep
`predictive_evidence []`; EC/name/keyword/Rhea/prose handles remain excluded-context admission
evidence and are never predictive. Next recommended action: mechanism-handle scout
**`atp_amide_ligase`** before any 23fp wiring; EC 6.3 is scope-only, and counted corroboration should
come from ATP/Mg or acyl-phosphate/amide-ligase Rhea participants, Ligase/ATP-grasp keyword/domain,
active-/binding-site evidence, or structure, with guards for kinases, biotin carboxylases, generic
ATP transferases, hydrolase side rows, and multi-fingerprint signals.

**2026-06-13 automation update: molybdopterin oxidoreductase 20fp expansion is now applied.**
After the cofactor-independent isomerase work below completed, the recommended next lane was first
scouted because prior supply was reaction-poor. The mechanism-handle scout over 80 reviewed UniProt
entries found strong non-EC evidence: molybdopterin/Mo-cofactor **80/80**, Rhea cross-reference
**78/80**, Mo feature/ligand context **65/80**, redox reaction text **49/80**, and oxo-transfer
reaction text **71/80**; boundary signals were explicitly recorded (flavin 33/80, heme 13/80,
peroxide/peroxidase 26/80). The lane was then wired as a deliberate 20-fingerprint universe change:
`molybdopterin_oxidoreductase` fingerprint + `molybdopterin_redox` ontology family, EC 1.*
oxidoreductase scope-only rule, molybdopterin/Mo-cofactor or Rhea redox/oxo-transfer or Molybdenum
keyword/domain or Mo-pterin active-/binding-/metal-site mechanism handles, hydrolase /
non-oxidoreductase side-EC / peroxide-peroxidase / biosynthesis / multi-signal guards, 20fp OOS
preregistration re-freeze, offline tests, non-destructive preview, then explicit apply. Live
preview/apply (`scripts/source_molybdopterin_oxidoreductase_family.py --max-records-per-lane 80
--apply`) fetched **255** reviewed Swiss-Prot rows, mechanism-corroborated **210**, admitted **207**
before cap, and appended **207** bronze rows; **3** were novelty-throttled, **41** were
disambiguation holds (`no_mechanism_corroboration`), **0** off-target fingerprint matches were held,
**4** were skipped, and duplicate skipped at apply was **0**. External bronze is now **4409** (was
4202 after isomerase); combined label surface is **5111**; frozen current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after apply. Honest
counters after the apply stay separate: **positive_bronze 3398**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k:
**6602**. Post-apply audit: **20 fingerprints**, fingerprint Gini **0.1613**, holes `[]`, only
`metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. All 207 added Mo rows have
`predictive_evidence []`; EC remains scope-only and is never counted. Follow-on scout
`artifacts/v3_copper_oxidoreductase_mechanism_handle_scout_current702_20260613.json` examined
**80** copper candidate entries with **0** fetch failures and found Rhea **78/80**, redox text
**77/80**, oxygen/oxidase text **78/80**, copper feature/ligand context **31/80**, explicit copper
cofactor comments **20/80**, and small heme/side-EC/glycosyltransferase boundary signals. Next
recommended action: design `copper_oxidoreductase` 21fp only from that scout, require non-EC copper
mechanism corroborators, and add explicit heme/flavin/molybdopterin/hydrolase/glycosyltransferase
boundary guards before any preview/apply.

**2026-06-13 automation update: cofactor-independent isomerase 19fp expansion is now applied.**
After the CoA work below completed, the recommended next lane was wired as a deliberate
19-fingerprint universe change and sourced through the same evidence-rich admission machinery. Added
`cofactor_independent_isomerase` fingerprint + `isomerization` ontology family, EC 5.3 scope,
Rhea isomerization equation text or Isomerase keyword/domain plus active-/binding-site/base
mechanism handles, non-5.3 side-EC guards, 19fp OOS preregistration re-freeze, offline tests,
non-destructive preview, then explicit apply. Live preview/apply
(`scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 80 --apply`) fetched
**266** reviewed Swiss-Prot rows, mechanism-corroborated **147**, admitted **142** before cap, and
appended **142** bronze rows; **5** were novelty-throttled, **70** were disambiguation holds
(`no_mechanism_corroboration`), **28** off-target fingerprint matches were held
(`nad_p_dehydrogenase`), **21** were skipped, and fetch failures were **0**. External bronze is now
**4202** (was 4060 after CoA); combined label surface is **4904**; frozen current702 remains **702**
with sha `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after apply.
Honest counters after the apply stay separate: **positive_bronze 3191**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k:
**6809**. Post-apply audit: **19 fingerprints**, fingerprint Gini **0.1613**, holes `[]`, only
`metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. The post-isomerase
non-destructive source-supply scout recommends **molybdopterin oxidoreductase** next:
**460** reviewed rows and **33** distinct full EC labels in a 200-row sample, ahead of
`copper_oxidoreductase` (**222** / **12**). Both are reaction-poor, so the next lane should start
with a mechanism-handle scout and explicit subclass/boundary guards, not a direct apply. Next
recommended lane: wire `molybdopterin_oxidoreductase` only if the scout confirms non-EC mechanism
corroborators (molybdopterin/Mo-cofactor, Rhea redox/oxo-transfer participants, Mo-pterin
domain/keyword, active-/binding-site metal/ligand evidence, or structure); keep EC scope-only and
re-freeze OOS preregistration to 20fp before any registry apply.

**2026-06-13 automation update: CoA acyltransferase 18fp expansion is now applied.**
After the non-heme iron 2OG work below completed, the documented next lane was wired as a deliberate
18-fingerprint universe change and sourced through the same evidence-rich admission machinery. Added
`coa_acyltransferase` fingerprint + `acyl_transfer` ontology family, EC 2.3.1 scope, CoA/acyl-CoA
Rhea participant or CoA/acyl-CoA feature text or Acyltransferase keyword/domain plus active-/
binding-site mechanism handles, hydrolase side-EC guards, 18fp OOS preregistration re-freeze,
offline tests, non-destructive preview, then explicit apply. Live preview/apply
(`scripts/source_coa_acyltransferase_family.py --max-records-per-lane 80 --apply`) fetched **218**
reviewed Swiss-Prot rows, mechanism-corroborated **204**, admitted **188** before cap, and appended
**188** bronze rows; **16** were novelty-throttled, **11** were disambiguation holds
(`no_mechanism_corroboration`), **1** off-target fingerprint match was held, **2** were skipped, and
fetch failures were **0**. External bronze is now **4060** (was 3872 after 2OG); combined label
surface is **4762**; frozen current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after apply. Honest
counters after the apply stay separate: **positive_bronze 3049**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k:
**6951**. Post-apply audit: **18 fingerprints**, fingerprint Gini **0.1652**, holes `[]`, only
`metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. A follow-on current
source-supply scout recommends **cofactor-independent isomerase** as the next lane: **5273** reviewed
rows and **51** distinct full EC labels in a 200-row sample, no reaction-poor warning. A mechanism
handle scout over 80 entries found catalytic activity context **80/80**, Rhea cross-reference
**62/80**, active-or-binding-site context **65/80**, and fetch failures **0**. It also surfaced
multi-EC boundary rows (`2.5.1.18`, `1.11.1.-` in the top sample), so the next runner needs explicit
mutase/racemase/epimerase/isomerase subclass guards and off-target holds. Next recommended lane: wire
`cofactor_independent_isomerase` as a deliberate 19fp universe change with EC 5.3 scope-only lanes
plus Rhea isomerization equation/participant or Isomerase keyword/domain and active-/binding-site/base
mechanism corroboration; add guards before any preview/apply.

**2026-06-13 automation update: non-heme iron 2OG 17fp expansion is now applied.**
After the P450 work below completed, the next documented scaling lane was wired as a deliberate
17-fingerprint universe change and sourced through the same evidence-rich admission machinery. Added
`non_heme_iron_2og_dioxygenase` fingerprint + `non_heme_iron_oxygenation` ontology family, EC 1.14.11
scope, Fe(II) plus 2-oxoglutarate/succinate/CO2 Rhea participant or Dioxygenase keyword/domain or
active/binding-site mechanism handles, heme/flavin/peroxide guards, 17fp OOS preregistration
re-freeze, offline tests, non-destructive preview, then explicit apply. Live preview/apply
(`scripts/source_non_heme_iron_2og_family.py --max-records-per-lane 80 --apply`) fetched **212**
reviewed Swiss-Prot rows, mechanism-corroborated **198**, admitted **172** before cap, and appended
**172** bronze rows; **26** were novelty-throttled, **12** were disambiguation holds
(`multi_fingerprint_signal_conflict` 5, `no_mechanism_corroboration` 7), **2** were skipped, and
fetch failures were **0**. External bronze is now **3872** (was 3700 after P450); combined label
surface is **4574**; frozen current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after apply. Honest
counters after the apply stay separate: **positive_bronze 2861**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k:
**7139**. Post-apply audit: **17 fingerprints**, fingerprint Gini **0.1657**, holes `[]`, only
`metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. A follow-on current
source-supply scout recommends **CoA acyltransferase** as the next lane: **7728** reviewed rows and
**82** distinct full EC labels in a 200-row sample, no reaction-poor warning. A CoA lane-design scout
then showed Acyltransferase keyword supply **7728**, `cc_cofactor:coa` supply only **23**, EC-only
ceiling **9981**, and **108** distinct EC labels in a 500-row sample. An 80-entry mechanism-handle
scout found Rhea cross-references **80/80**, CoA/acyl-CoA reaction text **72/80**,
active/binding-site context **56/80**, and fetch failures **0**. Next recommended lane: wire
`coa_acyltransferase` as a deliberate 18fp universe change with EC 2.3.1 scope-only lanes plus
CoA/acyl-CoA Rhea participant or Acyltransferase keyword/domain and catalytic His/Cys/active-site
mechanism corroboration; do not rely on UniProt `cc_cofactor:coa` alone. Add non-CoA transferase and
multi-fingerprint-signal guards, OOS re-freeze, offline tests, preview, then apply only if gates pass.

**2026-06-13 automation update: cytochrome P450 16fp expansion is now applied.**
After the SAM methyltransferase work below completed, the next documented scaling lane was wired as
a deliberate 16-fingerprint universe change and sourced through the same evidence-rich admission
machinery. Added `cytochrome_p450_monooxygenase` fingerprint + `heme_monooxygenation` ontology
family, EC 1.14 scope, heme plus O2/Rhea participant or P450/monooxygenase keyword/domain or
heme-thiolate mechanism handles, explicit non-peroxidase guard, 16fp OOS preregistration re-freeze,
offline tests, non-destructive preview, then explicit apply. Live preview/apply
(`scripts/source_cytochrome_p450_family.py --max-records-per-lane 80 --apply`) fetched **142**
reviewed Swiss-Prot rows, mechanism-corroborated **128**, admitted **110** before cap, and appended
**110** bronze rows; **18** were novelty-throttled/rejected, **14** were disambiguation holds, and
fetch failures were **0**. External bronze is now **3700** (was 3590); combined label surface is
**4402**; frozen current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after apply. Honest
counters after the apply stay separate: **positive_bronze 2689**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k:
**7311**. Post-apply audit: **16 fingerprints**, fingerprint Gini **0.1657**, holes `[]`, only
`metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. A follow-on focused scout
confirmed **non-heme iron 2OG dioxygenase** as the next strong lane: EC 1.14.11 + iron/dioxygenase
handle has **870** reviewed rows and a 200-row sample has **36** distinct specific ECs. That 17fp
follow-on is now applied in the update above; use the non-heme iron 2OG entry for current guidance.

**2026-06-12 automation update: SAM methyltransferase 15fp expansion is now applied.**
After the NAD(P)/glyco floor/cap work below completed, the next documented scaling lane was wired as
a deliberate 15-fingerprint universe change and sourced through the same evidence-rich admission
machinery. Added `sam_methyltransferase` fingerprint + ontology family, EC 2.1.1 scope, SAM/SAH Rhea
participant or Methyltransferase keyword mechanism handles, explicit no-Fe-S/radical-SAM guard,
15fp OOS preregistration re-freeze, offline tests, non-destructive preview, then explicit apply.
Live preview/apply (`scripts/source_sam_methyltransferase_family.py --max-records-per-lane 120
--apply`) fetched **315** reviewed Swiss-Prot rows, mechanism-corroborated **304**, admitted **264**
before cap, appended **250** bronze rows, and held **14** at the cap; **2** multi-fingerprint-signal
rows were held, **28** throttled as redundant, **12** rejected over-cap/no-new-chemistry, **9** skipped,
and fetch failures were **0**. External bronze is now **3590** (was 3340); combined label surface is
**4292**; frozen current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before/after apply. Honest
counters after the apply stay separate: **positive_bronze 2579**, **oos_bronze 1696**,
**silver_ready 0**, **silver_confirmed 17**, **projected 0**. Remaining positive-bronze gap to 10k:
**7421**. Post-apply audit: **15 fingerprints**, fingerprint Gini **0.1657**, holes `[]`, only
`metal_dependent_hydrolase` over-cap, next-batch floor deficit **0**. The new low-risk within-15fp
cap space for SAM is exhausted. Next recommended lane: **cytochrome P450 monooxygenase** as a
deliberate 16fp universe change because it has strong reviewed Swiss-Prot mechanism handles
(heme/thiolate cofactor + monooxygenase Rhea participant/EC 1.14 scope + P450 keyword/domain) and is
mechanistically distinct from `heme_peroxidase_oxidase`; wire spec/ontology/rule/tests/OOS re-freeze
before any preview/apply.

**2026-06-12 automation update: NAD(P)/glyco broadened-handle rows are now applied.** The
existing NAD(P)-dehydrogenase + glycosyltransferase runner was rerun deeper and applied to
the separate external bronze registry only. Batch 1 (`--max-records-per-lane 100`) applied
**373** rows: `nad_p_dehydrogenase` **0 -> 150** (chemistry-confusable cap reached; **113
held at cap**) and `glycosyltransferase` **0 -> 223**. Batch 2
(`--families glycosyltransferase --max-records-per-lane 150`) applied **27** more glyco rows,
taking `glycosyltransferase` **223 -> 250** (cap reached; **10 held at cap**). External bronze
is now **3340** (was 2940); frozen current702 remains **702** with sha
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`; combined label surface is
**4042** (was 3642). Honest counters after the apply stay separate: **positive_bronze 2329**,
**oos_bronze 1696**, **silver_ready 0**, **silver_confirmed 17**, **projected 0**. Remaining
gap to a 10k positive-bronze surface is **7671**; do not fill it by padding capped families.
The after-apply coverage audit reports fingerprint Gini **0.1578**, holes `[]`, only
`metal_dependent_hydrolase` over-cap, and next-batch floor deficit **0**. The 14-fingerprint
low-risk cap space for these two families was exhausted; the SAM methyltransferase 15fp lane above
is the completed follow-on.

Three findings from live recon refine the path below (none of them redefine the count to
make it "work"; see decision_log 2026-06-11/12):

1. **"Reviewed Swiss-Prot → 10k positive bronze" is false** (breadth feasibility scout):
   15/18 candidate families beyond the 12 are clean, but the clean capped supply projects
   to only ~4.7k positive bronze (gap ~5.3k). So 10k diverse POSITIVE bronze needs either
   broadened handles + source expansion, or honest re-scoping — **not** padding.
2. **Some shortage is an evidence-HANDLE problem, not supply** (evidence-handle scout):
   e.g. NAD(P) dehydrogenases (EC 1.1.1) have ~7800 reviewed entries but the `cc_cofactor`
   handle reaches 7; `keyword:NAD/NADP` reaches 7700 (NAD is a cosubstrate keyword, not a
   cofactor comment). **Fix within-Swiss-Prot handles BEFORE expanding source classes.**
3. **The honest counters stay SEPARATE.** Do NOT merge positives / OOS / silver depth /
   projections into one victory number; OOS and silver are different axes, projections are
   not real yet (`source_trust_tiers.HONEST_COUNTER_AXES`).

The refined path (replaces "reviewed Swiss-Prot → 10k bronze"):
**reviewed Swiss-Prot with broadened, family-specific MECHANISM handles + curated external
(tier 1) + carefully gated TrEMBL/UniRef (tier 2, N-of-M corroboration) + new family
ontology breadth (Stage 2) + the mandatory governor/novelty gate = diverse positive bronze,
with OOS and silver tracked separately.**

Discipline that makes this honest (do not violate):
- **Source trust tiers** (`source_trust_tiers.py`): only tiers 0–2 are bronze-eligible, with
  escalating N-of-M corroboration (1/2/3); tiers 3–4 (cluster/model projection) are
  hypotheses, never countable bronze. Trust tiers ADD a gate; the governor + novelty gate
  + dedup + leakage gate stay mandatory.
- **EC is scope-only, never a counted corroborator.** EC stays allowed for fetch / scope /
  stratification and `excluded_context`; the predictor is EC-free (features = cofactor
  identity, Rhea bond-change, active-site roles, geometry). Fetch broadly (EC/keyword),
  decide membership by **mechanism** evidence (Rhea, cofactor/cosubstrate, active-site,
  domain, cluster, structure). `evaluate_corroboration`'s counted axes exclude EC
  (`ec_scope_hint` is non-counted).
- **Next concrete step:** wire the broadened mechanism handles into the admission engine
  family-by-family (NAD(P)-dehydrogenase EC-subclass lanes, glycosyltransferase, …), via
  non-destructive preview → explicit `--apply`. See decision_log 2026-06-12 entries and
  `artifacts/v3_evidence_handle_expansion_current702.json` for the per-family winning handle.

---

## The one reframe everything depends on

**10k is not 10k rows. It is a balanced, non-redundant mechanism atlas where the
frozen 702 benchmark never moves and every label earns its place.** The repo's own
findings force this:

- Broad out-of-scope draining is **saturated** — a page-3/4 continuation over
  high-yield lanes "produced 2,793 continuation candidates but added **0** new
  candidate IDs"; the lesson is to split into new EC/keyword subqueries, not
  increase page depth (`decision_log.md`, handoff 2026-06-09).
- The positive classes are **30.8× imbalanced** (fingerprint Gini 0.51,
  positive:OOS 0.42) — coverage/redundancy governor, 2026-06-10.
- **26.7%** of what we already imported (456 of 1,710) would be re-throttled as
  near-duplicates by the novelty gate, concentrated in out_of_scope (373) and
  `metal_dependent_hydrolase` (71) — novelty gate self-audit, 2026-06-10.

So raw count is not the constraint; **diverse, honest supply is.** Chasing 10k of
the current 8 fingerprints by volume would manufacture redundancy and violate the
values.

---

## What is fixed, by our values (non-negotiable)

- **The frozen 702 benchmark is sacred.** `data/registries/curated_mechanism_labels.json`
  = 702 labels (562 in-distribution + 140 heldout); `coherence_audit_702` baseline;
  eval contract `sha256:731b94ebd3b4f7ae483a3cca75d2b8c3b88242024ecd9c364d70bdfcda6624ee`.
  All three are pinned by regression tests (`tests/test_geometry_artifact_regression.py`).
  The atlas grows in the **separate** expansion registry
  `data/registries/external_bronze_labels.json`; the benchmark is byte-unchanged. A
  v2 benchmark, if ever needed, is a **new** expert-reviewed freeze, never an edit of
  this one. The spent one-shot heldout read must not be re-run or tuned against
  (2026-06-04).
- **The leakage wall is absolute.** EC / protein-name / UniProt prose / curated text
  / `target_family_lane` stay in `excluded_context`, never predictive features; EC
  may decide **scope only**. Enforced in code by
  `labels._validate_external_out_of_scope_evidence_separation` and by
  `tests/test_leakage_closure.py`; the representation loop's featurizer has a unit
  test that mutates EC+name+lane+fingerprint and asserts the features are
  byte-identical.
- **The label gate is the only door in** (`src/catalytic_earth/`):
  `external_annotation_anchored_import.classify_row` (default = **HOLD**; a positive
  requires an annotation lane mapped to a fingerprint **and** the matching annotated
  cofactor class) → `labels.MechanismLabel.from_dict` (schema + leakage-separation
  validation) → `external_annotation_anchored_import.apply_external_annotation_anchored_import_to_registry`
  (dedup vs **both** registries, re-validate every label, **non-destructive
  append**, writes only the expansion registry). Nothing bypasses this. Review
  artifacts are **not** imports.
- **Bronze is honest.** `tier=bronze`, `review_status=automation_curated`,
  `evidence_basis=reviewed_swissprot_ec_rhea_cofactor_annotation`; structure/geometry
  confirmation is a **deferred** bronze→silver signal, not faked (2026-06-09 "the 10k
  unlock").
- **Do not scale model size.** The representation shootout settled it
  (`docs/wave1_representation_shootout.md`, 2026-05-26): ESM-2 150M (primary acc
  0.578), ESM-C, ProtT5, SaProt all **underperform** Foldseek (0.622) and the
  geometry baseline (1.000 on dense/near-orphan bins). "Do not scale models first."
  The Northstar Pivot (2026-05-31) showed the binding constraint is **feature
  overlap**, not the combiner. Use chemistry/geometry features only. The learned
  mechanism-feature embedding (Lever 2) is a recorded clean **negative** — it does
  not deployably beat geometry.
- **Safety scope** (`docs/safety_scope.md`): beneficial enzyme function only;
  outputs are hypotheses/candidates requiring wet-lab validation; never "confirmed"
  / "validated" without experimental backing.

---

## The pipeline (every new label runs this, in order)

```
reviewed UniProt/Swiss-Prot row (EC + cofactor + Rhea + active-site residues)
  → classify_row          scope from annotation; positive needs cofactor corroboration; else HOLD
  → governor              is this fingerprint/lane a hole / under-floor / over-cap?   (build-coverage-redundancy-audit)
  → novelty gate          admit only if it adds a new cluster/reaction/organism; throttle near-dups   (build-novelty-admission-gate-audit)
  → from_dict + writer    schema + leakage gate; dedup vs BOTH registries; non-destructive append
  → (later) promotion     bronze→silver ONLY via cofactor restoration/fusion, never apo geometry   (build-bronze-silver-promotion-preview)
```

The governor and novelty gate make growth diverse **by construction**; everything
else already existed. All four CLI tools above are non-destructive (write only to
`artifacts/` + `work/`, never a registry).

---

## The stages

### Stage 0 — Unblock sourcing (environment)
The cloud sandbox blocks UniProt (HTTP 403) and lacks mmseqs / ML backends, and the
hand-curated candidate pools are **drained**. A local/laptop env restores real
UniProt network and (on Mac) mmseqs. Nothing downstream proceeds without this.
Guardrails travel with the work regardless of env.

### Stage 1 — Close the holes (≈339 positive labels; highest value)
Source the holes and under-floor fingerprints to the **100-floor**, via targeted
EC/keyword **subqueries** (not deeper pages). Cap `metal_dependent_hydrolase` (308,
over the 250 ceiling, most redundant at 2.96 labels/distinct-reaction) — add none.

| fingerprint | combined | status | route |
| --- | --- | --- | --- |
| `ser_his_acid_hydrolase` | ~~42~~ **129** | **HOLE CLOSED (2026-06-11)** | cofactorless: EC 3.4.21/3.4.16/3.1.1, **no cofactor**, coordinate Ser-His-Asp triad corroborated against annotated ACT_SITE on the AFDB v6 predicted (apo) structure. Sourced to floor (+87 bronze) by `scripts/source_ser_his_hole.py --apply` (module `ser_his_hole_sourcing.py`). The one fingerprint the cofactor engine structurally can't reach — its corroborator is the triad geometry, not a cofactor. |
| `radical_sam_enzyme` | ~~10~~ **133** | **HOLE CLOSED (2026-06-10)** | disambiguation rule (Fe-S+SAM / CX3CX2C). Sourced to floor by `scripts/stage1_source_holes.py --apply` (+123 bronze); off the governor's hole list. |
| `cobalamin_radical_rearrangement` | ~~10~~ **144** | **HOLE CLOSED (2026-06-10)** | disambiguation rule (adenosylcobalamin + mutase EC 5.4.99/5.4.3/4.2.1.28/30/4.3.1.7). Sourced to floor (+134 bronze) after fixing the cobalamin matcher to read UniProt's inline-oxidation-state names (`cob(III)alamin`). |
| `flavin_monooxygenase` | ~~43~~ **116** | **CLOSED (2026-06-11)** | EC 1.14.13/1.14.14, flavin no-heme. Sourced to floor (+73 bronze). |
| `heme_peroxidase_oxidase` | ~~69~~ **119** | **CLOSED (2026-06-11)** | EC 1.11.1, heme. Sourced to floor (+50 bronze). |
| `flavin_dehydrogenase_reductase` | ~~87~~ **250** | **CLOSED (2026-06-11)** | EC 1.3/1.6/1.8.1, flavin no-heme. Sourced (+163 bronze) — high-yield/diverse space, filled to the 250 cap by the runner's cap guard (held the surplus rather than going over). |

Everything routes through the governor + novelty gate so orthologs are not
re-imported.

**Applied (2026-06-10 / 2026-06-11):** all five **cofactor-defined** Stage-1
fingerprints were sourced to the floor with live UniProt egress via
`scripts/stage1_source_holes.py --apply` (module `stage1_hole_sourcing.py`) —
fetch → cofactor/EC disambiguation → novelty gate → cap guard → non-destructive
preview, `--apply` appending bronze to the expansion registry only (frozen 702
untouched). Two holes (2026-06-10): `radical_sam_enzyme` 10→133,
`cobalamin_radical_rearrangement` 10→144 (+257 bronze; 1710→1967). Three under-floor
(2026-06-11): `flavin_monooxygenase` 43→116, `heme_peroxidase_oxidase` 69→119,
`flavin_dehydrogenase_reductase` 87→250 (+286 bronze; 1967→2253). Net: **7 of 8
fingerprints now BALANCED**; fingerprint Gini **0.51 → 0.2608**; combined 2412 → 2955.
The runner now enforces a hard per-fingerprint **cap guard** (≤250) so high-yield
spaces (flavin_DR) fill toward but never past the ceiling.

The cofactorless `ser_his_acid_hydrolase` hole (2026-06-11): sourced **42 → 129**
(+87 bronze; 2253 → 2340) via the dedicated `scripts/source_ser_his_hole.py --apply`
(module `ser_his_hole_sourcing.py`) — fetch serine-hydrolase rows (no cofactor) →
stage the **AlphaFoldDB v6** predicted coordinate → confirm the Ser-His-Asp triad
against the annotated ACT_SITE → novelty gate → apply. Its corroborator is the
coordinate triad, not a cofactor; the triad is present in the apo predicted structure,
which is why this fingerprint is apo-confirmable.

**Stage 1 is COMPLETE (2026-06-11):** the governor's hole list is **empty**; **all 8
fingerprints are at/above the 100-floor**; fingerprint Gini **0.51 → 0.1917**; combined
2412 → 3042 (frozen 702 untouched throughout). See decision_log 2026-06-10/2026-06-11
"Stage-1 …" and `docs/stage1_hole_sourcing_runbook.md`. The only remaining governor
flag is the intentional `metal_dependent_hydrolase` over-cap (308) — that is the
**Stage 2** on-ramp (its v2 split below), not a sourcing target. **Next:** Stage 2
(expand the family set — the real 10k lever), and triaging the existing held pools
(Pending candidate inventory above) through the same governor/novelty gate.

### Stage 2 — Grow the ontology (the bulk of the climb)
8 fingerprints × 250 cap ≈ **2,000 positives max** — so 10k honestly **requires more
mechanism families**. The coherence audit already flags this: `metal_dependent_hydrolase`
is a coarse bucket collapsing proteases/nucleases/phosphatases/deaminases, queued as
v2 splits. This is the repo's **Lever 4 — expand the family set**. Each new family /
v2 split is added the same disciplined way:

1. Define the fingerprint spec in `data/registries/mechanism_fingerprints.json`
   (cofactor chemistry + active-site residue-role signature + reaction-center bond
   change) and the family node in `data/registries/mechanism_ontology.json`.
2. Add a cofactor+EC rule to `external_cofactor_ec_disambiguation.DISAMBIGUATION_RULES`
   and lane mappings to `external_annotation_anchored_import.LANE_PRIMARY_FINGERPRINT`
   / `COFACTOR_FOR_FINGERPRINT`.
3. **Declare the family's deploy-missing active-site context type** — what the
   apo predicted structure *lacks* and how (or whether) to reconstruct it: cofactor,
   metal, substrate, PTM, oligomeric interface, ordered water, or **none** (e.g. a
   cofactorless catalytic-triad hydrolase loses nothing on apo). See "Reconstructing
   deploy-missing active-site context" below; this drives whether/how the family can
   ever reach silver.
4. Source annotation-anchored bronze under the governor + novelty gate.

Breadth of chemistry, not depth of one bucket, is where 10k comes from.

**Applied (2026-06-11) — first v2 split done:** `metal_dependent_hydrolase` was split into
four sub-families by reaction-center bond change — `metallopeptidase` (peptide C-N),
`metallophosphoesterase_nuclease` (phosphodiester P-O), `metallophosphomonoesterase`
(phosphomonoester P-O), `metallo_amidohydrolase_deaminase` (non-peptide amide/amidine C-N).
All four checklist items done: specs in `mechanism_fingerprints.json` (each declaring
deploy-missing context = **metal**) + ontology nodes; metal+EC disambiguation rules + lane
maps; governor signatures; and sourced to floor by `stage2_hydrolase_subfamily_sourcing.py`
(`scripts/source_stage2_hydrolase_subfamilies.py`) — 600 bronze admitted (150 each,
`--cap-ceiling 150`), expansion 2340 → 2940, combined 3042 → 3642, frozen 702 untouched,
Gini 0.1917 → 0.1518, seed positives 1346 → 1946. The coarse umbrella is KEPT for the
frozen-702 + pre-split expansion rows and gets **no new labels**. See decision_log
2026-06-11 "STAGE 2 STARTED". **Two honest caveats that gate further work:** (1) the
leakage-safe *chemistry* representation cannot yet separate the metal sub-families (they
differ by bond change, the deferred row-specific bond-change feature) — so these sub-families
are bronze-honest but not yet predictively separable; (2) the 8 → 12 positive-universe
expansion invalidated the 8fp OOS hard-negative pre-registration — it must be **re-frozen
for the 12fp universe** before the next OOS hard-negative import (Stage 3), and a clean
`label_factory_v1` ontology-version bump (currently still keyed `_8fp`) should accompany it.
A first split is sourced to **cap 150, not 250** — filling chemistry-confusable sub-families
to the ceiling manufactures the redundancy the plan warns against. Next splits/families:
glycosidases, and non-hydrolase chemistries (oxidoreductase/transferase) to keep chemical
breadth — hydrolysis now holds 6 of 12 fingerprints.

**Applied (2026-06-12/13) — broadened-handle transferase/redox/isomerase families filled:** the
first eight non-hydrolase broadened-handle families are now countable bronze, not just previews.
`nad_p_dehydrogenase` is capped at **150**, `glycosyltransferase` at **250**, and
`sam_methyltransferase` at **250**; `cytochrome_p450_monooxygenase` is at **110** and
`non_heme_iron_2og_dioxygenase` is at **172**; `coa_acyltransferase` is at **188**; and
`cofactor_independent_isomerase` is at **142**; `molybdopterin_oxidoreductase` is at **207**. All
meet the 100-floor and none should be sourced further without a new chemistry split. The coverage
governor reports no expansion holes; `metal_dependent_hydrolase` remains the intentional over-cap.
This raises positive_bronze to **3398** while keeping OOS/silver/projected counters separate. The
next breadth step should open **one new family** rather than deepen these: use the completed copper
mechanism-handle scout to design `copper_oxidoreductase`, then wire only if non-EC copper
corroborators and explicit heme/flavin/molybdopterin/hydrolase/glycosyltransferase boundary guards
are clean enough for a 21fp governance update, OOS pre-registration supersession, preview, and gated
apply.

### Stage 3 — Diverse OOS, novelty-gated
OOS is the abstention target and must keep growing in **coverage**, not redundancy.
Route every candidate through the novelty gate's cluster key
`(scope, full-EC, organism, sequence-length bin)`; admit only new
clusters/reactions/organisms. On Mac, upgrade the gate's metadata near-dup proxy to
true **mmseqs sequence clustering** — a strictly better dedup dimension than
metadata.

### Stage 4 — Bronze→silver promotion, the honest way
Promotion is gated by **deploy-missing active-site context presence in the
coordinates** — for the current cofactor-dependent families that means the cofactor,
and 103/104 of our coordinate-bearing rows are **apo** (cofactor absent), so the
geometry inverse-gate abstains on 100% of apo (the documented Problem-2 degradation;
experimental-apo and predicted-apo both abstain). So promotion does **not** wait for
more predicted structures — it waits on **reconstruction** of the missing context.
For the cofactor families the working lever is cofactor restoration/fusion
(restoration recovers 22/22 lost primaries; the fused sequence→cofactor channel
lifted heldout 23→37/45, one-shot **spent** — do not re-run). Run it (locally, with
backends) over the promotion preview's chemistry-corroborated queue; resolve the
**51 representation-loop review-outliers** (chemistry disagrees with the label)
first. Silver is earned per-row, never bulk-flipped. **Reconstruction is not
"cofactor" for every family** — see the next section.

### Stage 5 — A v2 benchmark, only when the atlas is broad
A 702-row benchmark over 8 families cannot validate a 10k atlas across many
families. When Stage 2 has matured the ontology, freeze a **new** expert-reviewed v2
benchmark (its own SHA; conjunctive win condition — mechanism prediction **and**
calibrated abstention on tail/hard-negative cases; cluster-bootstrapped, not
entry-bootstrapped). The current 702 stays frozen forever as the v1 anchor.

---

## Pending candidate inventory (as of 2026-06-09) — triage these before re-sourcing

A large multi-family intake already ran (Wave 2 + the seven family shards). **Nothing
was lost and almost nothing was force-imported** — the candidates are preserved as
preview/queue artifacts and sit behind the gate. Before sourcing anything fresh
(Stages 1–3), work these queues through the **governor + novelty gate** first; this
intake predates both, so expect a large fraction to be throttled as near-duplicates
or dropped as already-covered.

**The 12,495-candidate review surface** (`v3_external_import_review_preflight_current702_20260609.json`,
`terminal_state_counts`):

| terminal state | count | disposition |
| --- | --- | --- |
| `controlled_import_review_ready` | **275** | machine-clean; **queued for explicit human batch approval — not imported** (`v3_external_import_review_ready_preview_current702_20260609.json`) |
| `repairable_coordinate_blocker` | 5,179 | needs coordinates (network/local) |
| `hard_blocked_with_next_action` | 2,904 | blocked |
| `reject/OOS_preserve_signal` | 1,562 | rejected |
| `duplicate_external_conflict` | 1,275 | already in the expansion registry |
| `repairable_locator_blocker` | 1,096 | needs an active-site locator |
| `duplicate_current702_conflict` | 203 | already in the frozen 702 benchmark |
| `needs_structural_duplicate_screen` | 1 | — |

(275 ready + 12,220 in the repair/blocked queue, `v3_external_import_review_repair_queue_current702_20260609.json`.)

**What was imported from these pipelines (the 1,710 now in the registry)** — only the
cofactor-corroborated / clear-OOS / clean-screen rows passed the gate:
- 186 — original Wave 2 annotation-anchored import.
- 1,381 — scale-out **drain** of the already-materialized import-ready pools (2,426
  rows → 1,389 import decisions; **1,037 held** = 743 cofactor-confounded redox + 129
  no-cofactor + 107 ambiguous + 58 unmapped; `v3_external_scaleout_bronze_import_preview_current702_20260609.json`).
- 143 — cofactor/EC disambiguation recovering held redox/radical lanes (still **~730
  held** for lacking unique cofactor+EC corroboration;
  `v3_external_cofactor_ec_disambiguation_preview_current702_20260609.json`).

**Implications for the plan:** (1) the ~6,275 coordinate/locator-blocked rows resolve
in a **local env** (network/backends) — they are a Stage-0/1 unblock, not lost work;
(2) the ~1,478 duplicates and the held lanes are exactly what the novelty gate exists
to screen; (3) the 275 clean rows still require explicit human authorization +
label-factory gates (review ≠ import) — and should pass the governor/novelty gate
before any merge, so they grow diversity rather than re-saturate. Do **not** re-run
deeper-page sourcing on the same lanes (it added 0 new candidates last time); split
into new EC/keyword subqueries instead.

---

## Reconstructing deploy-missing active-site context (cofactor is the v1 instance, not the whole story)

This is a **parallel axis, not a stage**. The count/diversity stages above reach 10k
*bronze* labels and **do not need reconstruction at all** — annotation-anchored scope
decouples the label from geometry. Reconstruction is the **quality/deploy axis**: it
is what lets a label earn silver and what lets the atlas predict mechanism for novel,
unannotated sequences (the North Star). Run it where the count climb does not — and
do not confuse the two.

**The general problem (not "cofactor"):** the router was validated on experimental
active-site geometry but deploys on a predicted **apo** structure, which lacks
whatever active-site *context* the experimental one carried. Per the 2026-06-04
"Problem 2 Solution Architecture — Reconstruct Deploy-Missing Context From Sequence"
entry, verbatim: *"For the v1 families that context is the cofactor/metal; for future
classes it will be substrate, metal, PTM, oligomeric interface, or ordered water."*
So the lever is **"reconstruct the deploy-missing active-site context from the only
deploy-available signal (sequence), and abstain when you cannot"** — cofactor is the
first instance because the current eight are mostly cofactor-defined, **not** a
universal rule.

**Per-family, the missing context differs:**

- **7 cofactor-dependent fingerprints** (metal, PLP, flavin-monooxygenase, flavin-DR,
  heme, radical-SAM [Fe-S+SAM], cobalamin) — the missing context is the
  cofactor/metal. This is where the 22/22 `cofactor_apo_loss` came from
  (2026-06-03 "Predicted-Geometry Degradation Is Cofactor-Loss-Dominated").
- **`ser_his_acid_hydrolase` is cofactorless** — its catalysis is the Ser-His-Asp
  protein triad, which is *present in the apo structure*. **Nothing to reconstruct**;
  it degrades far less on apo, and its confirmation is the triad geometry itself
  (which is exactly why `build-ser-his-triad-locator-scan` runs on apo coordinates).
- **Even within cofactor families, not every row needs it.** Control in the
  decomposition: 13/23 correctly-called primaries also had an experimental cofactor —
  apo sufficed for them. The loss hits only rows where the cofactor is load-bearing
  for the geometry signal.
- **Future families (Stage 2)** declare their own missing-context type (Stage-2
  checklist item 3), possibly **none**.

**The two reconstruction paths (2026-06-04 architecture):**

- **Path A — sequence→context feature channel (default).** Predict the missing
  context (for cofactor families: cofactor presence) from sequence, **train/cal
  only**, and fuse it where the experimental `ligand_context` plugged into the router.
  Measured: in-distribution out-of-sample recovery **30/35 (70.6%)**, 0 regressions
  (`cofactor_presence_calibration.py` / `sequence_cofactor_channel.py`); the spent
  heldout one-shot went **23 → 37/45** (+14; OOS FP 12.3% → 25.9%) — **that read is
  spent; never re-run or tune against it.**
- **Path B — structure restoration (in reserve).** Graft a **canonical/template**
  context (not the experimental one) into the predicted apo pocket and recompute
  geometry. Idealized restoration recovers **22/22**; realistic rigid graft **19/22**
  (the 3 failures are distorted-*backbone* rows). numpy is available for the Kabsch
  superposition; `torch/esm/foldseek` are not in the cloud, so Path B runs locally
  (`predicted_geometry_recovery.py`).

**The discipline (so reconstruction does not become a leak):**

- **Leakage-safe supervision is non-negotiable:** train the channel on *structural*
  observations (ligand context), **never** the mechanism fingerprint / EC / Rhea /
  text — otherwise it is circular and leaky. Fit on train/cal only.
- **The experimental-cofactor graft is circular** — that cofactor is unavailable at
  deploy — so it is only an oracle / upper bound, never a deploy input. Deploy uses
  Path A (sequence-predicted) or Path B (canonical/template).
- **The metal head is the known systemic weak point** (cal AUC ~0.77, spurious 0.99
  on true flavin/heme rows) and the main driver of OOS over-opening; the 5 hard
  misses need cofactor **localization** (predict binding residues) or transplant, not
  more presence-channel tuning (2026-06-04 "Channel-Recall-Limited").
- **Precision discipline:** prefer the **recalibrated abstention threshold** (reaches
  the suppression dial's precision for free) over the suppression dial, which
  sacrifices in-scope recall (2026-06-09 step-4 entry;
  `cofactor_fusion_operating_point.py`).
- Reconstruction stays a **silver/deploy** signal, **never** a bronze entry gate.

**One-liner:** reconstruction does not get us to 10k labels — annotation-anchored
bronze does — it turns the 10k atlas into a deploy-grade mechanism predictor and lets
bronze earn silver; and the thing reconstructed is **family-specific** (cofactor
first, sometimes nothing).

---

## The honest caveats (so we don't fool ourselves)

- **The cap math is the real story.** 10k forces ontology breadth (Stage 2). If we
  refuse to expand families, the honest ceiling is ~2k positives + diverse OOS, and
  padding to 10k with redundant OOS would violate the values. Say so rather than hit
  10k dishonestly.
- **Promotion may stay mostly bronze** until cofactor restoration is run at scale —
  and that is fine. Bronze is an honest tier; silver is earned, not assumed.
- **Beware the "receding horizon"** (`docs/MAP.md`): per-row deployment-blocker
  grinds (Lever 3/4 chores) that the framing can manufacture infinitely. This plan
  is sourcing-and-diversity-bound, not blocker-bound; if a lever turns into infinite
  per-row chores, stop feeding it.

---

## Assets already built (this plan's tooling)

All merged to `main`, all non-destructive, leakage-safe, with tests:

- `coverage_redundancy_audit.py` — the governor (balance/redundancy + acquisition
  targets). CLI `build-coverage-redundancy-audit`.
- `ser_his_triad_locator.py` — Ser-His-Asp triad corroborator + acquisition contract
  for the ser_his hole. CLI `build-ser-his-triad-locator-scan`.
- `novelty_admission_gate.py` — online near-dup/saturation filter feeding the apply
  path. CLI `build-novelty-admission-gate-audit`.
- `mechanism_representation_loop.py` — leakage-safe chemistry representation
  (cofactor/ligand + residue roles; LOO self-consistency 0.895); triages promotion,
  proposes hole candidates. CLI `build-mechanism-representation-loop`.
- `bronze_silver_promotion_preview.py` — promotion queue gated on **cofactor presence
  in coordinates** (not provenance). CLI `build-bronze-silver-promotion-preview`.
- `stage1_hole_sourcing.py` + `scripts/stage1_source_holes.py` — Stage-1 runner that
  fetches fresh reviewed Swiss-Prot for the five cofactor-defined Stage-1 fingerprints
  (two holes + three under-floor) and chains pilot → cofactor/EC disambiguation →
  novelty gate → cap guard → non-destructive preview (`--apply` appends to the
  expansion registry). Needs live UniProt egress; wiring is offline-tested. Runbook:
  `docs/stage1_hole_sourcing_runbook.md`.
- `ser_his_hole_sourcing.py` + `scripts/source_ser_his_hole.py` — the cofactorless
  `ser_his_acid_hydrolase` runner: fetches serine-hydrolase rows (no cofactor), stages
  the AlphaFoldDB v6 predicted coordinate, confirms the Ser-His-Asp triad against the
  annotated ACT_SITE (`ser_his_triad_locator`), novelty-gates, and previews/applies.
  Needs live UniProt **and** AlphaFoldDB egress; wiring is offline-tested with a
  synthetic CIF.

---

## Sources & where to verify (read before acting)

Do not take any claim in this plan on faith — every one is traceable. `docs/decision_log.md`
is reverse-chronological (newest at top); cite entries by their **dated title**
(line numbers drift). The durable human handoff is `docs/project_state.md` +
`docs/decision_log.md` + `docs/session_decision_record_*.md`; `work/handoff.md` is an
**auto-generated hourly ledger** (skim for tactical state, do not treat as
decisions); `docs/artifact_index.md` maps artifact files.

| Plan element | Verify / more info |
| --- | --- |
| North Star, values, "done correctly", honesty culture | `docs/MAP.md`, `docs/research_program.md`, `docs/project_state.md`, `README.md` |
| Leakage discipline + heldout one-shot rule | `docs/agent_runbook.md`; `tests/test_leakage_closure.py`; enforced in `labels._validate_external_out_of_scope_evidence_separation` |
| Safety scope (beneficial-only, hypothesis language) | `docs/safety_scope.md` |
| Frozen 702 benchmark: count, coherence baseline, eval contract | `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json`; `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json` (hashes to `sha256:731b94ebd3b4f7ae483a3cca75d2b8c3b88242024ecd9c364d70bdfcda6624ee`); pinned by `tests/test_geometry_artifact_regression.py` (`label_count == 702`); split manifest `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json` + `…holdout_eval_1025_current702_split_assignment_repaired_20260525.json` |
| The 8 fingerprints (5 primary + 3 secondary) | `data/registries/mechanism_fingerprints.json`, `data/registries/mechanism_ontology.json`, `docs/mechanism_fingerprint.md`; primary/secondary split in the coherence-audit artifact |
| The label gate / code path | `src/catalytic_earth/labels.py` (`MechanismLabel.from_dict`, `load_labels`, `COUNTABLE_REVIEW_STATUSES`); `docs/label_factory.md` |
| Annotation-anchored bronze = the 10k unlock | `decision_log.md` 2026-06-09 "Annotation-Anchored Bronze Is An Accepted External Label Basis (the 10k unlock)"; engines `external_annotation_anchored_import.py` (`classify_row`, `_build_label`, the apply writer), `external_scaleout_bronze_import.py`, `external_cofactor_ec_disambiguation.py`; `docs/external_source_transfer.md`, `docs/ingestion_plan.md` |
| Diversity governor (imbalance, holes, caps, redundancy) | `decision_log.md` 2026-06-10 "Coverage/Redundancy Governor"; `coverage_redundancy_audit.py`; `artifacts/v3_coverage_redundancy_audit_current702_20260610.json` + `work/…md` |
| Novelty / saturation admission gate | `decision_log.md` 2026-06-10 "Novelty / Saturation Admission Gate"; `novelty_admission_gate.py`; its artifact/work |
| ser_his hole + triad locator | `decision_log.md` 2026-06-10 "Ser/Cys-His-Asp Triad Locator"; `ser_his_triad_locator.py`, `serine_active_site.py`; its artifact/work |
| Stage-1 hole-sourcing runner (radical_sam + cobalamin) | `decision_log.md` 2026-06-10 "Stage-1 Hole-Sourcing Runner"; `stage1_hole_sourcing.py`, `scripts/stage1_source_holes.py`, `tests/test_stage1_hole_sourcing.py`; `docs/stage1_hole_sourcing_runbook.md` |
| Representation loop (chemistry features) | `decision_log.md` 2026-06-10 "Mechanism Representation Loop"; `mechanism_representation_loop.py`; its artifact/work |
| **Do not scale model size** (ESM2 etc. not decision-grade) | `docs/wave1_representation_shootout.md`; `decision_log.md` 2026-05-31 "…Feature Overlap…(Northstar Pivot)" and "Sobering Operating-Point Reality"; `mechanism_feature_embedding.py` (Lever 2 clean negative) |
| Promotion preview + the cofactor-presence correction | `decision_log.md` 2026-06-10 "Bronze->Silver Promotion Preview" and "CORRECTION — Promotion Confirmability Is Cofactor PRESENCE…"; `bronze_silver_promotion_preview.py`; its artifact/work |
| Problem-2 degradation (45/45→23/45, apo cofactor-loss) | `decision_log.md` 2026-06-03 "Predicted-Geometry Degradation Is Cofactor-Loss-Dominated"; `predicted_geometry_robustness.py`; `artifacts/v3_predicted_geometry_failure_decomposition_current702_20260603.json` |
| Reconstruction architecture + the two paths | `decision_log.md` 2026-06-04 "Problem 2 Solution Architecture — Reconstruct Deploy-Missing Context From Sequence" |
| Cofactor restoration 22/22 · realistic graft 19/22 | `decision_log.md` 2026-06-04 "Cofactor Restoration Recovers 22/22…" and "Cofactor Graft Is Realistic For 19/22"; `predicted_geometry_recovery.py`; `artifacts/v3_cofactor_restoration_recovery_probe_current702_20260604.json` |
| Sequence→cofactor channel ~70% · heldout one-shot (SPENT) | `decision_log.md` 2026-06-04 "Cofactor Channel Recovers ~70%…", "HELDOUT ONE-SHOT SPENT…", "Leakage-Safe Cofactor-Presence Channel"; `cofactor_presence_calibration.py`, `sequence_cofactor_channel.py`; `artifacts/v3_in_distribution_predicted_geometry_recovery_current702_20260604.json`, `…heldout_oneshot_cofactor_fusion_blind_pass…json` |
| Metal head weak point · hard misses not channel-recoverable | `decision_log.md` 2026-06-04 "Cofactor Recovery Is Channel-Recall-Limited…" |
| Precision dial (recalibrated threshold > suppression) | `decision_log.md` 2026-06-09 "Step-4 Precision Side Measured…"; `cofactor_fusion_operating_point.py` |
| Predicted-geometry pipeline runbook | `docs/predicted_geometry_robustness_pipeline_runbook.md` |
| Sourcing status: drained pools, 275-row queue, page-depth lesson | `work/handoff.md` (latest), `work/NEXT_WORKS_northstar_20260531.md`, `docs/external_source_transfer.md` |
| Pending candidate inventory (12,495 review surface; what imported vs held/blocked) | `artifacts/v3_external_import_review_preflight_current702_20260609.json` (`terminal_state_counts`), `…import_review_ready_preview…json` (275 ready), `…import_review_repair_queue…json` (12,220), `…scaleout_bronze_import_preview…json` (1,381 import / 1,037 held), `…cofactor_ec_disambiguation_preview…json` (143 / ~730 held) |
| ePK NO-GO (do not revive without non-heuristic approach) | `docs/epk_heuristic_geometry_no_go_20260521.md`; `decision_log.md` 2026-06-06 |

If a reference here ever disagrees with the code or a newer decision-log entry,
**the newer decision-log entry and the code win** — update this plan, don't quietly
work around it.

---

## One-line summary

**Unblock sourcing → close the holes → broaden the ontology → diverse
novelty-gated OOS → earn silver by reconstructing each family's deploy-missing
context (cofactor first, sometimes nothing) → freeze a v2 benchmark when ready** —
all behind the frozen-702 wall, the leakage wall, and the governor.
