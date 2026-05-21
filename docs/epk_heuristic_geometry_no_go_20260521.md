# ePK Heuristic Geometry No-Go Memo

Date: 2026-05-21

Scope: eukaryotic protein kinase ATP gamma phosphoryl transfer (`epk_atp_gamma_phosphoryl_transfer`)

Status: review-only decision memo. No label registry, mechanism fingerprint registry, production scorer, threshold, artifact migration state, or import gate was changed by this memo.

## Decision

Stop the current ePK heuristic-geometry research loops as a production-activation path.

This is not a decision to abandon ePK permanently. It is a decision that the current strategy has produced enough evidence:

```text
Heuristic geometry-only ePK production activation: no-go.
Heuristics as candidate generators and safety guards: keep.
ePK future path: learned context model, cleaner active-state sourcing, or targeted source/wet-lab adjudication.
```

The current loops have successfully exposed the blocker. Continuing to add more review-only schema, gate, audit, or proxy-feature machinery would now risk turning the project into artifact accumulation rather than scientific progress.

## Why This Memo Exists

The original goal was to build a mechanism-level atlas that can support real enzyme-function decisions. For ePK, the project repeatedly tested whether compact source-free geometric rules could identify true kinase substrate-transfer evidence while rejecting sibling ATP-dependent enzymes and non-substrate mimics.

The answer is now clear enough for an operational decision:

1. Simple proximity rules recover some true positives but admit too many counterexamples.
2. Stricter source-free geometry reduces false positives but misses real positives.
3. More topology, contact, exposure, orientation, backbone, and acid/base features made the blocker more legible but did not clear it.
4. The policy and regression gates are useful, but they currently protect against false progress rather than enabling a countable ePK positive.

## Current Headline State

```text
countable ePK positives: 0
production ePK claims allowed: 0
label/fingerprint edits: 0
threshold calibrated: no
external hard-negative scored ePK re-audit: no
current recommendation: pause heuristic ePK loops
```

Latest federated/policy state:

```text
federated policy rows integrated: 14
federated entries integrated: 8
source leakage count: 0
unsafe control non-abstentions: 0
production claim allowed: false
progress claim allowed: false
```

The federated harness is working as a safety layer. It is not producing a countable positive.

## Initial Five Scientific-Blocker Agents

The first five scientific-blocker agents answered the broad blocker question. Their findings should be treated as completed evidence, not as questions to keep reopening.

| Agent / axis | Main finding | Operational meaning |
| --- | --- | --- |
| Substrate-role axis | No source-free substrate-role or substrate-identity axis is ready for a frozen ePK policy. | Substrate identity is the central unresolved biology/representation blocker. |
| Ligand-state policy | ATP/ANP/AMP-PNP active-gamma states can be frozen only as review-only policy. ADP, product, and substrate/acceptor analog states remain review-only. | Product/analog/split rows cannot be counted as active-gamma false negatives or positives. |
| Sibling counterfamily stress | Current controls block distance-only thresholding but are not enough for production activation. ASKHA, dNK, GHKL, GHMP, and ATP-grasp remain insufficiently covered for production breadth. | Sibling risk is real and independent of substrate-identity risk. |
| External stress tranche | The tranche is useful as review-only stress regression. Only `4EKK` was primary fresh nonrepeat; most others were already regression-context rows. | Do not use this tranche for clean held-out performance claims. |
| Strict/permissive geometry evaluation | Strict rule had one decisive false positive and missed positives; permissive nearest-hydroxyl admitted nearly every counterexample. | Distance/proximity is not substrate-role identity. |

## Core Geometry Results

The strongest direct evidence against heuristic geometry-only ePK is the strict/permissive rule comparison:

```text
strict source-free rule:
  TP = 7
  FP = 1
  TN = 10
  FN = 4
  decisive FP = 7B56

permissive nearest-hydroxyl rule:
  TP = 9
  FP = 11
  TN = 0
  FN = 2
```

Interpretation:

```text
Tight geometry loses real positives.
Loose geometry admits controls.
The missing variable is not just a better distance cutoff.
The missing variable is biological substrate-role identity.
```

## Decisive Positive and Negative Rows

Rows that repeatedly shaped the decision:

| Row | Role in evidence |
| --- | --- |
| `1IR3` | Current protein-substrate positive retained by several review-only surfaces. |
| `5HVK` | LIMK/cofilin source-valid review evidence; ANP PG to cofilin Ser3 was measured near enough to be interesting, but local Mg/Mn context was absent for strict active-gamma admission. |
| `6Z3R`, `8OXM`, `8OXO` | Short-peptide positives. These are easier than folded-protein substrate cases. |
| `1O6K`, `1O6L` | Review leads from AMP-PNP/Mg peptide-context evidence, useful but narrow. |
| `9UUR`, `9UUX` | Folded Tyr/MEK-ERK-like positives that collide with source-free counterexample structure classes. |
| `9UW4` | Counterexample sharing folded Tyr reciprocal-context signatures with `9UUR`/`9UUX`. |
| `7B56` | Decisive false positive for relaxed polymer/folded substrate role rules; also an internal-fragment/topology mimic. |
| `2JJ2` | F1-ATPase/large-chain local-ligand decoy; blocks generic topology assumptions. |
| `4HPU` | Split-state/topology counterpressure; evidence should not be fused across contexts. |
| `7CAG`, `8BMS`, `7ZDT`, `7ZE5` | Transporter/topology and ATP/ANP/Mg false-positive pressure. |
| `5UJ7:biological_assembly_1` | Pinned context-v4-only biological-assembly split failure. |

## Positive-Evidence Lane Findings

The positive-evidence lane found source-relevant and chemically interesting rows, but no clean active-state candidate satisfying the needed conditions.

Needed for a clean active-state candidate:

```text
active_gamma coordinate state
terminal gamma donor
local Mg/Mn or equivalent catalytic metal context
native or near-native protein Ser/Thr/Tyr acceptor
same-structure kinase/substrate context
no acceptor mutation invalidating the source site
no product/analog/split-state blocker
no unresolved topology/substrate-role ambiguity
no sibling/ATPase/transporter counteraxis hit
no source leakage
```

Representative positive-lane results:

| Surface / row | Finding | Blocker |
| --- | --- | --- |
| LIMK1/cofilin `5HVK` | ANP PG to cofilin Ser3 OG at 4.236 A; source-valid LIMK/cofilin authority recovered. | No local Mg/Mn on strict donor; review-only. |
| LIMK1/cofilin `5L6W` | AGS PG to cofilin chain C Cys3 SG at 3.573 A. | Source Ser3 phosphoacceptor is mutated to Cys; no local Mg/Mn. |
| Haspin/H3 `4OUC` | Modeled H3 Thr3 source-site context recovered. | No active donor or transition analog under scanner; donor fields null. |
| TGF/BMP receptor-SMAD | Source-only PDB surface reviewed. | No active-gamma or transition-analog candidate rows. |
| EphA3, MKK4/p38, LRRK2/Rab, eIF2alpha-family, transfer-alias/literature surfaces | Multiple source surfaces were explored. | No clean local-metal active-gamma native-acceptor candidate admitted. |

The positive lane is therefore not empty, but its output is source-site/review signal, not production-admissible ePK evidence.

## Substrate-Role Identity Findings

The substrate-role lane repeatedly tested source-free features:

```text
gamma/acceptor distance
cross-chain topology
auth-terminal/internal-fragment status
reciprocal entity context
local exposure
orientation/asymmetry
backbone continuity
contact interface
acid/base carboxylate proximity
coordinate-state taxonomy
```

Latest acid/base proximity run:

```text
candidate/state rows reused: 211
PDB-level conflict rows reused: 54
phosphoproduct rows reused: 135
acid/base proximity rows emitted: 220
mixed positive/counterexample acid/base signatures: 8
```

Latest coordinate-state counts in that lane:

```text
active_gamma = 205
adp_state = 5
ambiguous_coordinate_state = 1
ligand_absent = 4
product_state = 4
split_state = 1
```

Latest blocker classes:

```text
topology_ambiguity = 109
active_gamma_geometry = 71
none = 19
product_state_evidence = 9
ligand_materialization = 6
substrate_role_identity = 4
internal_fragment_mimicry = 1
split_state_evidence = 1
```

Decisive substrate-role conclusion:

```text
9UUR and 9UUX reciprocal Tyr candidates have gamma-coupled carboxylate contacts.
9UW4 counterexample candidates also have those contacts.
```

So acid/base proximity, like the earlier topology/contact/backbone probes, is useful review-routing evidence but not source-free substrate-role identity.

## Sibling and False-Positive Evidence

Sibling controls show that ePK-like ATP/gamma geometry overlaps many non-ePK families.

Examples from the sibling counterfamily review:

```text
NDK: 4 gamma/Mg homolog controls, mapped catalytic His distances 2.899-3.339 A.
PfkB: 9 controls, PG-to-family-acid/base distances 3.872-5.596 A.
PfkA: 5 controls, PG-to-family-acid/base distances 3.611-5.534 A.
ATP-grasp: 2 measured controls, both collide with the 6 A candidate cutoff.
```

The nearest-gamma-to-oxygen source-free rule false-hit 11 of 20 measured NDK/PfkA/PfkB/ATP-grasp sibling controls:

```text
1TZ6, 1WKL, 3Q86, 3R5F, 4XYJ, 5C1O, 5XZ8, 8W2H, 8W2J, 9OAN, 9PFY
```

The later sibling runtime surface is valuable as a guard:

```text
runtime oracle rows: 119
weak proximity false-positive controls: 85
product/ADP/analog/split-state review-only controls: 24
unsafe non-abstention count under expected policy: 0
```

The false-positive hunter expanded the adversarial surface:

```text
latest refreshed regression rows: 355
source artifacts: 26
unsafe non-abstentions after expected policy: 0
```

However, this is not a positive ePK result. It shows the policy layer is preventing false progress. It also shows why proximity-only ePK is unsafe.

Pinned false-positive lesson:

```text
5UJ7:biological_assembly_1 falsifies context-v4-only biological-assembly sufficiency.
```

Additional metric-seeded split contexts such as `9FXK`, `6TXC`, `6TXE`, and `3PKP` now stand as abstention controls.

## Policy Harness Findings

The policy harness successfully enforced source separation and review-only status:

```text
forbidden source leakage: 0
unsafe control non-abstentions: 0
labels/fingerprints changed: false
production_claim_allowed: false
```

The v7 federated contract locked candidate identity, coordinate state, claim status, and entry rollups. A later v9 adapter found real rows for `adp_state`, `ligand_absent`, and `unavailable_coordinate_state`, but it did not change any production candidate status.

This is exactly the drift risk:

```text
The policy machinery is now good enough to classify review-only states.
More harness/schema work without candidate status changes is not a scientific win.
```

## Ligand-State Decision

The ligand-state policy can remain as a future prospective review-only boundary:

Predictive only if all conditions co-materialize in the same structure:

```text
ATP/ANP/AMP-PNP active-gamma donor
terminal gamma-equivalent atom
local Mg/Mn-compatible metal
catalytic-site locality
pre-frozen source-free acceptor/role features
```

Review-only, not predictive:

```text
ADP/Mg
product-state ADP plus phosphorylated product/substrate
SEP/TPO product context
substrate/acceptor analogs such as B31/KAN-like context
active-state nucleotide structures missing terminal gamma, metal, or source-free acceptor/role evidence
cross-PDB split-state repair
source-reviewed kinase/substrate role as a predictive feature
```

## What This Proves

This does not prove ePK is impossible. It proves the current hand-built heuristic-geometry strategy is not enough for broad production activation.

The true blocker is candidate-level biological role:

```text
Is this hydroxyl the real substrate acceptor,
or merely a nearby residue, chain, fragment, sibling-family atom, product-state marker, or topology mimic?
```

Compact source-free geometry has not answered that reliably for folded-protein and kinase-kinase cases.

## What Should Stop Now

Stop these ePK activities unless a new mandate explicitly restarts them:

```text
new ePK schema versions
new generic federated scoreboards
new broad review-only audits
new proximity/contact/backbone/orientation/acid-base feature probes
new broad source-surface scans that only emit review-only rows
new sibling/false-positive gates unless a real unsafe route is being pinned
```

The current ePK agents should not keep running just to produce:

```text
more review-only rows
more missing-state adapters
more gate-count growth
more blocker descriptions
more broad source exhaustion packets
```

## What Can Restart ePK

ePK should restart only with one of these concrete goals:

1. Learned context pilot:
   - use heuristics only to enumerate candidate gamma/acceptor pairs;
   - learn richer context from sequence, structure, interface, local graph, metal/phosphate geometry, and sibling-family hard negatives;
   - evaluate on frozen candidate classes with source leakage blocked.

2. Clean active-state candidate search:
   - search specifically for an active-gamma/local-metal/native Ser/Thr/Tyr acceptor in a same-structure kinase/substrate context;
   - stop immediately if the surface is exhausted.

3. Terminal class decision:
   - permanently mark a class review-only unless specific external/source/wet-lab evidence appears.

4. Wet-lab or expert-adjudication bridge:
   - define a small candidate set whose ambiguity cannot be resolved from current coordinates;
   - ask exactly what experiment or expert source review would decide it.

## Learned Context Model Direction

A learned context model should not replace the policy guards. It should replace the failed idea that one compact hand-built geometric proxy can decide substrate role.

Practical design:

```text
1. Enumerate candidates deterministically:
   structure -> gamma sites -> Ser/Thr/Tyr acceptor candidates

2. Build candidate-level features:
   local phosphate and metal graph
   kinase fold context
   acceptor-chain local sequence window
   interface geometry
   chain and entity relationship
   active-site residue arrangement
   structure-neighbor context
   sequence embeddings
   sibling-family hard-negative tags

3. Train/rank:
   true ePK transfer candidates vs sibling ATP-dependent controls,
   ATPase/transporter controls,
   same-chain/internal-fragment mimics,
   product/analog/split-state rows,
   and source-reviewed positives kept out of predictive text features.

4. Gate:
   hard policy still blocks source leakage, product/analog/split misuse,
   sibling unsafe non-abstention, threshold tuning, and candidate-specific repair.

5. Evaluate:
   freeze candidate selection before scoring,
   report retained positives, abstentions, hard-negative leakage,
   and decision-changing failures.
```

This keeps what worked:

```text
heuristics as filters
policy as safety
hard negatives as guardrails
source review as adjudication
```

and stops what did not work:

```text
another hand-crafted ePK geometry proxy
```

## Bottom Line

The current ePK effort produced real scientific evidence:

```text
Distance-only is unsafe.
Strict geometry is incomplete.
Product/analog/split states must remain review-only.
Sibling ATP-dependent controls overlap ePK-like geometry.
Folded-protein substrate role is underdetermined by compact coordinates.
The policy harness prevents false claims but does not create positives.
```

Therefore:

```text
Pause the current ePK heuristic research agents.
Preserve the artifacts as a no-go evidence base.
Do not resume ePK until the next effort is a learned-context pilot,
a clean active-state sourcing attempt,
or a targeted source/lab decision campaign.
```

