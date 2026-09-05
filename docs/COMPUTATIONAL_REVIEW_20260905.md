# Computational review — 2026-09-05

> **Successor review, 2026-09-05:** read
> [Computational development review](COMPUTATIONAL_DEVELOPMENT_REVIEW.md) for
> current permissions and adjudications. This first-pass report is preserved
> as review history. The successor narrows several panel holds and corrects
> the first-pass DHFR rationale: M0112 is exact only at the implemented
> reaction-core scope, with narrower source applicability. The earlier
> aggregation/bifunctional-scope statement does not control current use.


This is an agent assessment and corrective work, with a public-source trail.
It does not fill or resolve the frozen human-review submissions. The July
Phase A/B packages remain historical checkpoints. Their all-unreviewed state
must not obscure the concrete computational findings here.

## A0A177THN5: withdraw the donor-specific transfer

**Decision:** withdraw the APX-specific transfer from structural neighbour
P48534 and retire the larger APX-versus-CcP study that depended on it. Preserve
class-I-like heme peroxidase as a family-level hypothesis. CcP-like is the
provisional working interpretation, not established target-specific activity.
This is an already exposed June 29 candidate, not a new validation surface.

The public evidence supports a narrower conclusion than either a definitive
APX or CcP assignment:

- The live [UniProt record](https://rest.uniprot.org/uniprotkb/A0A177THN5.json)
  identifies a 313-residue *Tilletia indica* protein, unreviewed and inferred
  from homology. Entry version 32 retains sequence version 1. It does not
  establish physiological electron-donor specificity.
- The [InterPro IPR044831 definition](https://www.ebi.ac.uk/interpro/api/entry/interpro/IPR044831/)
  includes both yeast Ccp1 and Arabidopsis APX1–6. Its `Ccp1-like` label is
  therefore not a discriminant between them. A tempting annotation-based
  replacement of the APX claim with a definitive CcP claim would repeat the
  original over-transfer.
- [Meharenna et al. (2008)](https://doi.org/10.1021/bi8007565) show why close
  fold agreement does not determine reducing-substrate specificity: substrate
  access/binding and the radical environment matter. The June 29 global
  structural similarity and common catalytic residues cannot establish APX
  donor chemistry.
- [Patterson et al. (1995)](https://pubmed.ncbi.nlm.nih.gov/7703248/) identify
  a porphyrin radical in APX despite its conserved proximal Trp. Trp presence
  alone does not establish a CcP-type radical intermediate in this target.

[Machine-readable evidence and inspection limits](../data/diagnostics/peroxidase_reassessment_20260905.json)
record the retrieved API response hashes and selected metadata. UniProt and
InterPro receive source attribution; summaries are project-authored. Article
inspection used public abstracts/indexed excerpts, not a claim of complete
paper review. No new model, alignment, pocket calculation, assay, kinetic
measurement or spectroscopy was performed. Private correspondence is not
published or presented as public evidence.

The residual donor question is worth reopening only when a concrete use needs
it. The current atlas work does not depend on completing this retired study.

## Atlas-50 correction proposals

The [57-row crosswalk assessment](ATLAS50_COMPUTATIONAL_CROSSWALK_REVIEW.md) and
[40-case panel assessment](ATLAS50_COMPUTATIONAL_PANEL_REVIEW.md) separate
local consistency checks, refreshed primary-source checks, and scientific
inference. Per-row inspection depth prevents a source-transcription pass from
being mistaken for a complete mechanistic review.

The crosswalk pass flags **16 rows for correction**, leaves **26 unresolved
because their relation targets are insufficient**, and gives **15 provisional
assessments**. These are triage dispositions, not accuracy estimates or expert
votes. In particular, 32 rows have no populated source slot because the draft
search index covered only selected cases. This is an acquisition limitation,
not a demonstrated absence from the source databases.

| Priority | Concrete finding | Correction to carry forward |
|---|---|---|
| 1 | PLP row uses M0049, a pyruvoyl-dependent histidine decarboxylase | Reject that anchor and its derived lookup bundle. M0482 is a verified PLP candidate but non-detailed; it cannot supply ordered steps. |
| 2 | Heme bucket includes laccases and uses P450cam M0133 as its sole M-CSA anchor | Move copper-laccase scope to the copper row; use a direct peroxidase anchor such as M0239, with P450 overlap explicit. |
| 3 | Class-II aldolase rationale claims M0052/M0222 pairing but the packet omits M0222 | Include M0222 explicitly as same-EC/different-mechanism counterevidence in a successor draft. |
| 4 | Broad DHFR fingerprint is labelled an exact duplicate of one bacterial M0112 object | Withdraw exact equivalence at that scope; distinguish the conserved-water N5 proton donor from Asp26's network role. |
| 5 | Serine/metallo beta-lactamase scopes are broader than their anchor coverage | Separate class-specific mechanisms; use verified M0015/M0016 as class-B1 candidates rather than a source-gap claim. |

The panel pass verified source transcription for **40/40 candidates** and
performed deeper reaction/structure checks on **six**. It recommends additional
holds on three proposed inclusions: **M0064 topoisomerase III** (DNA topology),
**M0106 pyruvate dehydrogenase E1** (tethered carrier context), and **M0107
carbon monoxide dehydrogenase** (coupled component/cofactor state). These are
requests to demonstrate a consistent representation, not proof that the cases
are impossible to represent.

The three existing exclusions remain held. M0753 needs a source-scope
correction first: the exact M-CSA/2A0N handle describes HisF with free ammonium,
not the full HisH–HisF coupled channel. M0970 also contains a non-ChEBI polymer
product placeholder and an inconsistent polymer flag. Retaining the nominal
47-case July proposal does not make its pass assumptions scientifically settled.

The concrete human decision set can be grouped into three discussions:

- **What is the comparison object?** Name the source object and exact relation
  target before adjudicating duplicate, specialization, aggregation or bridge.
  This addresses the 26 targetless rows together instead of repeating the same
  schema ambiguity in 26 forms.
- **What state belongs inside one mechanism?** Decide consistently how
  carrier-tethered reactions, coupled components, and polymer/topology state
  fit the shared representation. A source identifier matching the draft does
  not answer this question.
- **Where does source applicability stop?** For the few high-impact examples,
  identify which donor, cofactor, class and elementary-step claims the exact
  source supports. Preserve counterexamples and abstain beyond that boundary.

These findings are a correction overlay. They do not silently rewrite the
content-bound July packets or treat automated agreement as human approval.
They should accompany any use of the old candidate proposal.

## How work proceeds while human review is pending

1. Correct demonstrably wrong source locators and scope descriptions in a
   separately versioned successor draft, retaining the original packets and
   an explicit old-to-new change map. Resolve donor/cofactor mismatches before
   spending on structures or assays. Existing curated702 labels are search
   leads, not independent support for replacement mappings.
2. Write one shared representation contract for each disputed type of state,
   with examples that pass and examples that explicitly abstain. Start with
   tethered carrier/reaction instances and polymer/topology state because
   they affect currently passing panel cases as well as the three exclusions.
   Do not fix a case by inventing family-specific fields.
3. Ask humans only the remaining source-applicability, mechanistic-granularity,
   and representation questions, with exact evidence beside each question.
   Keep straightforward locator corrections out of a 97-form burden. Preserve
   the formal attestation needed for eventual gate closure without requiring a
   scientist to interact with JSON during substantive discussion.
4. Keep independent annotation and a selection freeze as separate later
   decisions. The frozen Phase B acquisition plan is not executed by this
   assessment. Bounded public-source reads here support correction proposals;
   no acquired record is admitted as a new mechanism or gold label.

No benchmark was rescored, protected registry expanded, follow-on mechanism
compiled, source-acquisition budget approved, or outside message sent by this
work. Computational review reduces known errors and the human decision load;
it does not provide the missing independent annotation.

## Rosalind setup and execution provenance

Rosalind Workbench `0.2.5-research-preview` was installed and confirmed enabled
through the official app CLI. The official macOS installer was also downloaded
and its disk-image checksums verified. Workbench is a launcher; its local
plugin exposes app-only launcher/settings tools, not a headless scientific
review model in this task. No GPT-Rosalind inference is claimed. These
assessments were performed by the current Codex agents using repository data
and public primary sources.

The [official Workbench documentation](https://developers.openai.com/blog/rosalind-workbench)
distinguishes Explore mode from organization-gated Research mode. Plugin
installation does not establish this account's Research-mode entitlement.
