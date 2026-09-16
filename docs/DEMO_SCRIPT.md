# Demonstration script — 90 to 120 seconds

A shot list for capturing the running application. Not a video engine, and not a
second implementation of anything.

**Rules for the capture.** Every frame is a real screen recording of the running
application. The fixture-labelled segment currently in the rehearsal clip must
not appear in the final sequence positioned as a live suite result. If no
authorized suite capture exists by recording time, cut Act 3 entirely and say
native inspection is pending — a 75-second honest clip beats 110 seconds with a
relabelled fixture.

---

### Act 1 — the question (0:00–0:20)

| | |
|---|---|
| **Screen** | Terminal, then the workbench evidence panel for H297N. |
| **Action** | Type `catalytic-earth atlas-mechanism-evidence --variant H297N --endpoint isotope_exchange`. Let the JSON land. |
| **Caption** | "H297N mandelate racemase shows no detectable racemase activity." |
| **Caption** | "Does that mean catalysis is gone?" |

Hold on the two returned observations. Enlarge them.

### Act 2 — the chemistry answers it (0:20–0:50)

| | |
|---|---|
| **Screen** | The two isotope-exchange rows, then the mechanism replay panel. |
| **Caption** | "(S)-mandelate: alpha-proton exchange **retained**, 3.3-fold below wild type." |
| **Caption** | "(R)-mandelate: **not detected** — and nondetection is not zero." |
| **Caption** | "Selective impairment, not total loss. PMID 1909893." |

Pause two full seconds on the retained-exchange row. This is the outcome; give
it room.

Then one beat on the boundary — this is the differentiator, not a disclaimer:

| | |
|---|---|
| **Caption** | "1MNS is reference geometry. There is no H297N mutant structure here — and the record says so itself." |

### Act 3 — native inspection (0:50–1:15) — *only with a real capture*

| | |
|---|---|
| **Screen** | The actual external suite performing the structure/source operation. |
| **Action** | Run it, let it return, then **open the returned artifact from its row** in the case card. |
| **Caption** | "The saved output, opened from the case it answers." |
| **Caption** | "Structural citation PMID 8292591 — a different source role. Recorded as separately sourced context, not a match." |

If there is no capture: skip to Act 4 and caption "Native inspection: pending."

### Act 4 — it generalises (1:15–1:40)

| | |
|---|---|
| **Screen** | Terminal, second case. |
| **Action** | `python scripts/query_atlas_perturbations.py --comparison tk_2020:H473N:DHB_accumulation` |
| **Caption** | "Different enzyme, same path, no new code." |
| **Caption** | "H473N stopped making the competing product — and made **less** target product. 5.5 vs 10.5 mM." |
| **Caption** | "The obvious inference was wrong. The record catches it." |

### Close (1:40–1:55)

| | |
|---|---|
| **Screen** | `catalytic-earth claims` output. |
| **Caption** | "Every result ships with what it does not claim." |
| **Caption** | "Clone, build, reproduce: START_HERE.md" |

---

## Delivery notes

- The rehearsal clip is silent and moves fast. Narrate or caption throughout;
  captions alone are fine.
- Lead with the question, never with architecture. No one is moved by a module
  diagram.
- One idea per caption. Read each aloud — if you run out of breath, cut it.
- Do not spend the clip explaining metadata fields.
- Numbers on screen must match the briefs in `docs/briefs/` exactly.
