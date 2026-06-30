# Atlas extension — where the unique capability actually lives (scoping, 2026-06-30)

The decisive orphan search showed the atlas's unique claim ("mechanism where sequence is blind")
is **not demonstrable for its current 4 families**, because those mechanisms inhabit
sequence-recognisable superfamilies. This scopes the only direction where the unique capability
*can* exist — and, importantly, where it may be demonstrable **for free (compute), without a lab.**

## The principle
The atlas beats sequence **only** for mechanisms that are **sequence-cryptic** — the *same
catalytic chemistry realised across unrelated sequences and folds* (convergent evolution). There,
sequence/Pfam have no homology to transfer from, but the **active-site geometry** (the catalytic
constellation — residue identities + 3D arrangement) is conserved. The current validated channel
matches on **whole-fold similarity** (foldseek TM), which is sequence-correlated and therefore
cannot cross those boundaries. The unique capability requires matching on **active-site geometry**,
not fold.

## The concrete example (real, checkable)
The **Ser-His-Asp catalytic triad** is the textbook convergent mechanism. It appears in multiple
*unrelated* superfamilies that share **no sequence and no fold**:
- **PA clan / trypsin fold** (PF00089) — what the atlas currently samples;
- **SB clan / subtilisin fold** (PF00082);
- **SC clan / α/β-hydrolase fold** (PF00561, lipases/esterases).

A trypsin, a subtilisin, and a lipase do the *same* serine-hydrolase chemistry, but BLAST/Pfam/fold
matching to one will **never** find the others. A geometry channel that detects the Ser-His-Asp
constellation **would** catch all three. This is exactly the regime the current atlas misses.

## The extension
1. **Switch retrieval to active-site geometry.** The modules already exist in the repo
   (`serine_active_site`, `metal_active_site`, `plp_active_site`, `geometry_retrieval`,
   `geometry_head`) but were **not** the validated channel. Wire them into a calibrated,
   abstaining geometry-NN retrieval.
2. **Target convergent mechanisms.** Start with **catalytic triads / protein-only active sites**,
   because their geometry is detectable on **apo AlphaFold models** (no ligand needed). Cofactor
   mechanisms (metal/heme/PLP) need holo structures — defer them.
3. **Curate multi-fold references.** For each convergent mechanism, include reference members from
   *each* fold it appears in, so geometry — not fold — drives recognition.

## The decisive demonstration — FREE, no wet lab
This is the key payoff: the unique capability may be provable **computationally**.
> **Cross-fold mechanism recovery.** Give the geometry channel **only trypsin-fold (PA) references**
> and ask it to recognise a **subtilisin-fold or α/β-hydrolase-fold** serine hydrolase — proteins
> that are *sequence- and fold-unrelated* to the references. Pre-register the baselines (BLAST /
> Pfam / fold-NN) which **must fail** cross-fold. If geometry recovers the mechanism where they
> can't, the unique capability is **demonstrated in silico**, isolating the atlas — no lab, no money.

A held-out **fold** (not just a held-out protein) is the unit; recovery across the fold boundary is
the metric.

## Honest constraints (this is research, not a quick win)
- The geometry channel's reliability is **unproven** — prior predicted-geometry work hit robustness
  and abstention-signal problems (`docs/predicted_geometry_robustness_pipeline_runbook.md`, the
  `predicted_geometry_*` artifacts). Wiring it up is real work.
- Apo AlphaFold models limit geometry detection to **protein-only** active sites first.
- Gold for convergent mechanisms exists in M-CSA (mechanism + catalytic residues per entry) but
  needs **curation** to group one mechanism across its folds.
- Effort: weeks of compute + curation. **Cost: compute only.** No lab, no spend.

## First step
Quantify convergence in M-CSA: for the catalytic-triad mechanism, enumerate the distinct Pfam
clans/folds it appears in, and assemble a multi-fold reference + a held-out-fold test set. That
turns this scoping into the cross-fold recovery experiment above.
