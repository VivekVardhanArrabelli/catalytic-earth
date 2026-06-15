# Discovery & de novo — strategy notes (2026-06-15)

A conversation-derived strategy record (not a code change). It captures how we think about
the atlas's relationship to "de novo," what the data empirically supports, and the resulting
direction. Future agents: treat this as orientation, and re-test the empirical claims against
the live registry before leaning on them.

## 1. Emergence: dataset vs model (the precise form)

De novo capability does NOT emerge from raw atlas row count. A label atlas is not a generative
model; it does not "wake up" at 100k rows and design enzymes. But it is also wrong to say
emergence is purely a model property — datasets have threshold effects too. The precise form:

- A dataset's threshold is **task-relative, not intrinsic.** There is no abstract count at
  which the atlas "becomes capable." There is a **coverage density** at which a *specific
  downstream operation* becomes reliable, and the threshold differs per operation:
  reliable nearest-neighbour retrieval needs >=k grounded examples per region; calibrated
  uncertainty needs enough boundary coverage to know where confidence should fall off;
  active-learning yield needs coverage dense enough that uncertainty sampling stops chasing
  noise.
- So the honest phrasing: *raw count does not create de novo capability; sufficient diverse,
  grounded coverage opens new operating regimes for retrieval / representation / calibration /
  active-learning — where "sufficient" is defined by the downstream operation, never the count.*
- This matches the repo's own lesson: continuation over high-yield lanes saturated, and the
  governor/novelty gate became necessary because redundant orthologs stopped adding
  information. In information terms the novelty gate is an **effective-sample-size** gate:
  high count, near-zero marginal information. The binding constraint is information, not rows.

## 2. "De novo" splits into two very different claims

- **A. De novo enzyme DESIGN** — generate a new sequence/backbone that performs a target
  chemistry. Model-central, far. The atlas is NOT the generative substrate here; it is a
  grounding / constraint / evaluation layer around structure/design/generative models. Today's
  de novo enzyme design emerged from *structural/sequence* scale at the *model* level
  (RFdiffusion / ProteinMPNN / AlphaFold-class), not from a mechanism-label atlas.
- **B. De novo mechanism DISCOVERY / annotation** — find proteins that sit outside known
  mechanism regions but carry coherent cofactor / active-site / reaction-center evidence, and
  flag them as candidate new families/subfamilies. Atlas-central, near-term. The repo already
  has the primitives: centroids, `propose_for_fingerprint`, out_of_scope ranking, the novelty
  gate, promotion triage.

Caveats that keep B honest:
- B still runs through a model: "project the atlas onto 100M-1B sequences" needs a
  sequence->mechanism projection. The capability lives in *that* representation; the atlas is
  the grounding/eval layer that lowers its hallucination and bounds its claims. Do not let
  dataset-emergence sneak back in via B.
- The representation is biased toward what it knows. "Coherent" is judged by a representation
  trained on known families, so a genuinely novel mechanism can look *incoherent* (low
  cohesion) and get filtered as noise, while a **coverage gap** (a known family not yet
  sampled) looks coherent and gets flagged as "discovery." Most of what B surfaces is **novel
  recombination of known mechanistic features**, not new feature *types*.

## 3. The two-axis discovery idea (and the trap)

To stop discarding new chemistry as "low cohesion noise," separate two axes that the current
gate conflates:

1. **Evidence quality** — how strong is a row's own mechanistic evidence (resolved active
   site, real/balanced Rhea reaction, holo cofactor presence), *independent of any family
   match*.
2. **Family match** — cohesion to the nearest centroid.

The interesting quadrant is **high evidence + low match to everything** — coherent, grounded,
unlike anything known. Silver grounding is the precondition: you can only trust "well-evidenced
and unlike anything" if the evidence is silver-solid, not bronze-noisy.

THE TRAP (learned the hard way on 2026-06-15): an evidence score that counts "has a recognised
bond-change class" as evidence **bakes in the known-vocabulary bias** — it can only ever surface
coverage gaps, never new chemistry (true novelty has no recognised bond-change and would score
low). Evidence quality MUST be **vocabulary-independent** (structure + reaction presence/balance),
and the new-chemistry flag is the opposite of what that mistaken score rewarded: a real reaction
+ a well-resolved site whose reaction-center is NOT classifiable by any known primitive, far from
all families.

## 4. What the data actually showed (read-only probe, 2026-06-15)

A non-destructive probe over the live registry (evidence-quality vs nearest-centroid match):

- **Sanity check passed:** of ~6,196 seed rows (assigned to families), essentially none were
  flagged high-evidence-but-unlike-anything (1, borderline). The method does not cry "novel"
  at known chemistry.
- **Out_of_scope discovery pool:** a tight, **replicated** cluster of 8 rows, identical
  chemistry signature (no cofactor, no metal, phosphodiester hydrolysis), far from every
  centroid. Honest interpretation: **a coverage gap, not new chemistry** — metal-INDEPENDENT
  phosphodiesterases (the atlas has a metal-DEPENDENT phosphoesterase family but no
  cofactor-free one). A real win for ontology completion; not world-novelty.
- With the corrected vocabulary-independent evidence definition, the "unclassifiable
  reaction-center" candidates (17) were, on inspection, also known chemistry our *classifier*
  lacks a class for: beta-glucosidase (`DIMBOA beta-D-glucoside + H2O = DIMBOA + D-glucose`,
  replicated x4), ester hydrolase, N-ribosyl hydrolase. "Unclassifiable by our code" almost
  always means **our vocabulary is incomplete**, not new-to-the-world.

## 5. The honest floor

To claim *new chemistry* you must rule out *all known* chemistry. The atlas's ~41 fingerprints
+ ~20 bond-change primitives are a sliver of known enzyme chemistry (thousands of reaction
types). So "unlike anything in the atlas" is, with overwhelming prior probability, "known but
unsampled," not "new." A credible world-novelty claim would require benchmarking a candidate
against a COMPREHENSIVE reaction reference (full Rhea ~15k reactions, KEGG, MetaCyc, BRENDA) —
and even "absent from Rhea" means "uncharacterised," not "impossible." Confirmation is wet-lab.
The atlas can point at a well-formed, well-evidenced, replicated **unknown** (the door); it
cannot certify world-novelty or characterise what is behind the door.

## 6. The decision (direction)

**Continue scaling — and it is the right call, not a deferral.** Discovery is bottlenecked by
our own incompleteness, and the scaling we are doing (adding diverse new families + silver
grounding) IS ontology completion — it directly shrinks that bottleneck. A broader, silver-
grounded atlas makes a future "unlike anything known" candidate genuinely meaningful. Revisit
the new-chemistry question seriously once the ontology is comprehensive enough that "novel" is
a strong word; we are far from that (41 vs hundreds of mechanism types), so scaling now is
correct.

Two refinements so it compounds:
1. Keep "scaling" meaning **diversity + grounding**, never bronze ortholog count (the governor/
   novelty gate enforces this — keep it enforced).
2. Use the **read-only discovery probe as a compass**, not a separate project: it is free
   (no registry writes, no collision) and ranks the highest-evidence MISSING families/
   primitives, so it aims the scaling at the gaps that matter (e.g. it already pointed at
   metal-independent phosphodiesterase and an unmodeled glycosidase cluster). Discovery steers
   scaling rather than competing with it.

Operational caution: there are two automations writing the same sharded registry. Only one
driver should own registry writes at a time (use `.git/catalytic-earth-automation.lock`);
read-only probes (like the discovery compass) are always safe to run alongside.

## 7. Concrete next steps this implies (not yet done)

- Turn the read-only probe into a proper **ontology-completion discovery queue**: leakage-safe,
  non-colliding artifact that ranks high-evidence/low-match clusters (with replication) as
  candidate missing families/primitives for review. (The two found 2026-06-15 are the first
  entries: metal-independent phosphodiesterase; an unmodeled glycosidase cluster.)
- Make the reaction-center vocabulary more compositional (graph-edit primitives: bonds
  formed/broken, charge/electron changes) so "novelty" is a continuous residual rather than an
  out-of-vocabulary miss — this raises the classifier's ceiling toward, but never to, true
  new-chemistry detection.
- These are additive to the silver-grounding + diverse-family scaling already underway; they
  do not replace it.
