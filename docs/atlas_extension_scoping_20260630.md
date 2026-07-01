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

## ⚠️ Correction (2026-06-30): the geometry channel is NOT a fresh, sequence-independent path
An earlier version of this doc oversold "activate the geometry channel." The existing
`predicted_geometry_recovery` harness shows its recovery mechanism **is the sequence cofactor
channel**: holo geometry works (45/45) → **apo** AlphaFold drops it to 23/45 (cofactor missing from
the model) → the **sequence cofactor-presence channel** recovers it (fused). So for **cofactor
mechanisms, active-site-geometry recovery == cofactor recovery** — same lever, and NOT
sequence-independent on apo structures. Known limitations already on record: the geometry channel has
**no abstention signal** (10k eval) and modest accuracy (76% coarse / 31% exact), so it would forfeit
the atlas's one proven virtue (fail-safe abstention).

**Only genuinely non-redundant piece:** protein-only catalytic constellations (Ser-His-Asp triads)
have *no cofactor to be missing*, so apo triad geometry is the one case that is truly
sequence-independent. Everything else here is cofactor recovery re-labelled. Treat the triad-cross-fold
idea below as a **long shot that inherits the no-abstention weakness**, not the clean free win.

## The extension
1. **Switch retrieval to active-site geometry.** The modules already exist in the repo
   (`serine_active_site`, `metal_active_site`, `plp_active_site`, `geometry_retrieval`,
   `geometry_head`) and were **already studied** — for cofactor families this is the cofactor-fusion
   recovery (see correction above), so it is **not new** there. The only untried angle is
   **protein-only triad geometry**, and it must first be shown to carry an abstention signal at all.
2. **Target convergent mechanisms.** Start with **catalytic triads / protein-only active sites**,
   because their geometry is detectable on **apo AlphaFold models** (no ligand needed). Cofactor
   mechanisms (metal/heme/PLP) need holo structures — defer them.
3. **Curate multi-fold references.** For each convergent mechanism, include reference members from
   *each* fold it appears in, so geometry — not fold — drives recognition.

## The decisive demonstration — FREE, no wet lab
This is the key payoff: the unique capability may be provable **computationally**.

> **Cross-fold mechanism recovery.** References = the atlas with an **entire fold removed** (e.g.
> remove the trypsin/PA-clan serine hydrolases). Queries = **independent gold**: SwissProt
> experimentally-characterised serine endopeptidases (EC 3.4.21, label independent of structure) from
> the **held-out folds** (subtilisin PF00082, α/β-hydrolase PF00561). Pre-register the baselines
> (BLAST / Pfam / fold-NN, query→references) which **must fail** cross-fold. If the active-site
> **geometry** channel recovers the mechanism where they can't, the unique capability is
> **demonstrated in silico**, isolating the atlas — no lab, no money.

**Do NOT grade on M-CSA.** M-CSA appears only as the **reference set** (that is the atlas, which is
unavoidable and not circular). The **evaluation/query set is independent** (SwissProt/EC), exactly as
in the gold held-out — never M-CSA-vs-M-CSA.

**Hold out a whole FOLD, not a protein.** A held-out protein within the same fold ("recognise a
trypsin from trypsin references") is something sequence/fold baselines also pass — it proves nothing
unique. Removing an entire fold from the references and querying it forces the test to measure the one
thing only geometry can do: bridge a sequence- and fold-boundary the model never saw.

## Honest constraints (this is research, not a quick win)
- The geometry channel's reliability is **unproven** — prior predicted-geometry work hit robustness
  and abstention-signal problems (`docs/predicted_geometry_robustness_pipeline_runbook.md`, the
  `predicted_geometry_*` artifacts). Wiring it up is real work.
- Apo AlphaFold models limit geometry detection to **protein-only** active sites first.
- Gold for convergent mechanisms exists in M-CSA (mechanism + catalytic residues per entry) but
  needs **curation** to group one mechanism across its folds.
- Effort: weeks of compute + curation. **Cost: compute only.** No lab, no spend.

## First step
1. Enumerate the distinct folds/Pfam-clans the Ser-His-Asp triad spans (PA / SB / SC …) — using
   M-CSA + Pfam **only to define the fold map and the reference anchors**, not to grade.
2. Assemble reference triad enzymes per fold (the atlas side) and an **independent** query set
   (SwissProt EC 3.4.21 in the held-out folds).
3. Run cross-fold geometry recovery with the pre-registered failing baselines. That is the free,
   in-silico, atlas-isolating experiment — the legitimate successor to the deferred wet lab.
