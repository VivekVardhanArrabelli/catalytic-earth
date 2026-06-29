# Session Decision Record — 2026-06-29

Consolidates the 2026-06-29 work: turning the validated fold channel into
benchtop candidates, de-risking them, and climbing the **last non-lab validation
rung** (independent gold beyond M-CSA). Machine artifacts named below are the
source of truth; `docs/decision_log.md` holds the dated rulings.

All refs in sync at session end: work pushed on `claude/continue-last-commit-ytktge`
and merged into `main` (clean fast-forward).

---

## 1. Headline outcomes

1. **First GOLD off-M-CSA validation (PASS).** A leakage-safe, pre-registered,
   content-hashed (`54119a7d…`) held-out whose labels come from **experimental EC**
   (independent of structure) was spent once: in-scope recovery **45/64 = 0.703**
   (bar ≥ 0.70), OOS false-positive **2/72 = 0.028** (bar ≤ 0.40). Decomposed:
   heme **16/16**, PLP **14/16**, ser_his **13/16** generalise off-M-CSA on gold
   (43/48 = 0.90); **zero confident misroutes in any family** — every miss is a
   safe abstention, so when the channel commits it is right (45/45 in-scope,
   2/72 OOS). The system **fails safe**.

2. **metal_dependent_hydrolase is a coverage gap, not a precision failure**
   (2/16 recovered, **14/16 abstained, 0 misrouted**): the held-out used EC 3.4.24
   metalloendopeptidases (metzincin/gluzincin) while the atlas family is
   metallo-β-lactamase-fold-centric. The family is effectively "MBL-fold metal
   hydrolase." Actionable fix: add metzincin/gluzincin representatives.

3. **A genuine novel-target pipeline exists.** The validated fold channel was run
   over **uncharacterized** proteins (no EC, "Uncharacterized protein", predicted
   existence) → confident mechanism calls on proteins nobody has characterized,
   then de-risked by active-site verification.

---

## 2. The work, in order

| Artifact | Finding |
|---|---|
| `v3_gate3_lab_candidate_shortlist_current702_20260629` | Off-M-CSA confident calls assembled + UniProt-enriched. **Honest finding: all 112 are already-characterized Swiss-Prot** → a validation set, not a discovery set. 2 flavo-diiron multi-cofactor cases surfaced; 9 P14779 label-transfer artifacts flagged. |
| `v3_gate3_novel_dark_target_shortlist_current702_20260629` | Fold channel over **genuinely uncharacterized** proteins (5 atlas-family Pfams): 326 dark → 239 confident calls. MBL-fold dark proteins largely **abstained** (gate does real work). 11-target family-spread shortlist. |
| `v3_gate3_active_site_verification_current702_20260629` | De-risk before lab: **6 verified, 2 partial, 3 not-verified.** Serine triads resolved with catalytic H-bond geometry; di-zinc cluster 7/7; ascorbate-peroxidase 5/5; PLP/BioA 4/4. **All 3 flavin candidates failed** despite TM 0.85–0.93 (catalytic residues degraded) — false positives caught for $0. |
| `v3_swissprot_pdbholo_gold_heldout_preregistration_current702_20260629` | Independent gold held-out FROZEN (136 rows; EC-derived labels; 1,839 exclusions). Committed before any structure fetch. |
| `v3_swissprot_pdbholo_gold_heldout_eval_result_current702_20260629` | **PASS** (Headline 1). |

---

## 3. Decisions / claims

1. **Deployable claim widened** from "M-CSA only" to **"validated on independent
   gold for heme, PLP, and serine-hydrolase mechanisms, with fail-safe abstention;
   metal-hydrolase coverage limited to the MBL fold."**
2. **The non-lab validation ladder is now exhausted.** Gold exists only for
   already-characterized proteins; discovery and dark/novel-distribution validation
   are **lab-only**. The next genuine increment requires the bench.
3. **No registry/threshold/held-out mutation** all session; every step read-only.

---

## 4. Honest limitations

- The gold held-out validates **characterized** enzymes; it cannot certify calls
  on uncharacterized proteins or enable discovery.
- The aggregate PASS margin is thin (0.703) and carried by 3 strong families;
  metal is a known coverage gap.
- The novel dark-target shortlist is **Pfam-implied** (broad fold pre-selected);
  the fold/atlas + active-site steps add confidence and the specific assay, not
  mechanism-from-nothing.
- flavin excluded from the gold in-scope set (no unambiguous EC signature; failed
  active-site verification).

---

## 5. Forward

- **Lab pilot (next real step):** the 6 active-site-verified dark targets — see
  `docs/lab_pilot_guide_20260629.md`. A single confirmation is the first gold,
  prospective, off-M-CSA, dark-protein label the project could have.
- **Atlas fix (non-lab, optional):** add metzincin/gluzincin representatives to
  close the metal coverage gap, then re-validate on a NEW pre-registered held-out.
- Discipline carried forward: the M-CSA one-shot and this gold held-out are
  **spent**; any new operating point needs a NEW pre-registration against a NEW
  held-out. Do not grow fingerprint families without authorization.
