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
