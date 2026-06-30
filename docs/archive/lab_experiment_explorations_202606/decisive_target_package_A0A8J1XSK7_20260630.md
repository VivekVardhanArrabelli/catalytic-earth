# Decisive-experiment package — target A0A8J1XSK7 (2026-06-30)

The single target to express and assay. Self-contained for a bench scientist.

## Honest status of this target (read first)
- **Dark:** UniProt `A0A8J1XSK7`, *Owenia fusiformis* (a marine polychaete worm),
  "Uncharacterized protein", no EC, no experimental function. **The answer exists
  nowhere — the lab is the first ground truth.**
- **Sequence-divergent, but twilight not orphan:** best sequence identity to *any*
  characterised atlas enzyme is **28%**. This is the most divergent confident call
  available from current data. At 28%, sequence-homology mechanism-transfer is
  **unreliable but not impossible** — so this is far more decisive than a vanilla
  Pfam-confirm, yet it is **not** a fully sequence-blind orphan (<25%). A pure
  orphan target needs a deeper search (see end).
- **Atlas-confident + active-site verified:** structural match TM **0.90** to
  L-ascorbate peroxidase (P48534); **5/5 catalytic residues conserved** (distal
  His106, proximal His232, catalytic Arg102, Trp248, Asp301).

## The prediction (made by the atlas, not by an LLM)
**A0A8J1XSK7 is a heme-dependent peroxidase** (class-I/ascorbate-peroxidase-like),
using a heme iron with a distal His/Arg pair for H2O2 activation. This call is the
output of foldseek-vs-atlas + the validated TM≥0.70 gate + the catalytic-residue
check — a specific, falsifiable mechanistic hypothesis with named residues.

## What to send / order
- **Sequence:** `docs/decisive_target_A0A8J1XSK7.fasta` (369 aa, single domain).
- **Structure (reference):** `https://alphafold.ebi.ac.uk/files/AF-A0A8J1XSK7-F1-model_v6.cif`
- **Construct:** full length, single domain; N- or C-His tag. Codon-optimise for
  *E. coli* (invertebrate source). Express **apo**, reconstitute with **hemin**.
- **Order:** codon-optimised synthetic gene in pET-28a(+) (Twist/IDT/GenScript).

## The assay + what to look for
- **Positive readout:** peroxidase activity — oxidation of **ABTS** (420 nm),
  **guaiacol** (470 nm), or **ascorbate** (290 nm) in the presence of **H2O2**.
- **Cofactor confirmation:** heme Soret band ~**405 nm** after hemin reconstitution.
- **Specificity controls:** (1) omit H2O2 → no turnover; (2) apo (no heme) → little/
  no activity; (3) heat-denatured enzyme → no activity.
- **Success = predicted activity present, H2O2- and heme-dependent.** That confirms
  the atlas's mechanism call on a protein nobody had characterised.

## The baseline panel — pre-register BEFORE the assay (this isolates the atlas)
Record each, timestamped, so a positive can be credited to the atlas alone:
1. **BLAST / Pfam vs M-CSA / characterised enzymes** — note the best hit and its
   identity (expected: weak, ~28%, borderline; document whether it would transfer
   the *specific* mechanism).
2. **A protein language model (ESM function head)** — record its prediction/abstention.
3. **A frontier LLM given only the bare sequence (no name/organism)** — record its
   guess and confidence.
4. **The atlas** — the specific call above.
The experiment's value scales with how badly 1–3 do. (At 28% identity expect them
to be weak/uncertain, not silent — hence "twilight," and hence the honest caveat.)

## How the result is used
- **Confirmed** → first prospective, off-benchmark confirmation that the atlas
  assigns correct mechanism to a dark, sequence-divergent protein → justifies
  scaling and is the asset for funding/collaboration.
- **Not** → bounds the confident-call reliability in the divergent regime; redirect
  to the atlas's proven twilight-zone + fail-safe value.

## For a PURE sequence-blind (orphan) target
Not available from the current Pfam-selected dark pool (0/239 below 25% identity —
by construction, since Pfam selection requires family-level sequence similarity).
Finding a true orphan (<25%, sequence-blind) needs a **clan/superfamily or
Pfam-negative dark search** (fold a broad un-family-selected pool, keep confident
structural matches that are sequence-orphan). That is the next compute step if a
maximally-decisive target is wanted.
