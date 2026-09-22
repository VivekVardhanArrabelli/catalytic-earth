# Internal reuse evaluation, 22 September 2026

The bounded pilot supports **revise before expansion**. Atlas preserved one
material curation qualification missed by source-only reading, but the two
comparisons reached the same broad decisions and Atlas used more observed time.
This does not establish that the proposed four-week useful-reuse programme is
complete or that Atlas improves scientific decisions generally.

## What was compared

Four existing Sol/ultra threads plus a coordinator ran two internal tasks at
fixed revision `8988939104dba5015270958935f53ec5b5bf859e`. The answer routes
received the same question and retained primary packet; the Atlas route could
also use its existing compiled records, queries and briefs. Separate agents
established source references before reading either final answer. Answers were
locked before adjudication. These are related-model computational checks.

| Task | Source-only, assignment to final | Atlas, assignment to final | Result |
| --- | --- | --- | --- |
| ThDP activation/reset reuse, M0106 and M0219 mechanism 1 | 540.336 s; 4 shell blocks | 771.418 s; 34 shell blocks | Same localized-reuse decision; Atlas adds the material partial-activation qualification |
| E317Q annotation across experimental endpoints | 138.579 s; 3 shell blocks | 192.580 s; 4 shell blocks | Same revise decision and essential replacement; no demonstrated material quality advantage |

Elapsed times come from app turn metadata. The narrower first/last-tool windows
in the workers' logs exclude some reasoning and writing and are not substituted
for this metric. Shell batching differs. Neither observed time nor command
counts establish causal efficiency or human effort savings. Prior curation,
implementation and maintenance hours are unknown; no break-even estimate follows.

### ThDP: a real qualification, unchanged broad decision

The frozen question asked whether Atlas-50 row 30 could admit shared localized
activation and reset modules for M0106 mechanism 1 and M0219 mechanism 1, with
mapped actors/arrows, exceptions and transfer limits. Both routes supported
localized reuse and kept the complete parent mechanisms separate.

Activation compares M0106 step 1 with M0219 step 1. The selected actor graphs have
35 versus 34 atoms. M0106 includes an explicit H `a65` bonded to mapped N
`a64`, with no M0219 counterpart. Excluding that H while retaining its boundary
gives a 34-atom/34-covalent-bond projection and all five directed arrow matches.
Activation is therefore partial/qualified, without equal full actor or
protonation state. The H is absent from retained source flows; this says nothing
about physical inactivity. Reset, M0106 step 7 versus M0219 step 6, matches all
34 selected actors, 34 covalent bonds and five arrows without an excluded atom.

Atlas explicitly retained that activation exception. The source-only answer
correctly mapped the reactive arrows but omitted the qualification. It did
**not** expressly claim full actor-state isomorphism, so the omission is not
scored as an explicit false claim. It matters for relation typing, even though
both answers recommend localized activation/reset reuse.

Neither answer supports metal/geometry, physical atom identity, homologous
residue, whole-state or whole-cycle transfer. Adjacent inferred panels also
differ: M0106 returns His/water while M0219 describes extra-enzymatic product
cyclization. Row 30 remains unreviewed; this comparison does not promote it.

Evidence: the retained
[M0106 packet](../../data/atlas/source_drafts/sources/M0106.json),
[M0219 packet](../../data/atlas/source_drafts/batches/aldolase-transketolase/sources/M0219.json)
and their original manifests/attribution. The Atlas route also used the existing
[ThDP correspondence](../ATLAS_THDP_CORRESPONDENCE.md).
These M-CSA annotations and schemes are not complete experimental papers.
The Atlas arm remembered the prior partial-activation/exact-reset conclusion;
source-only reported less relevant prior exposure. Atlas additionally performed
broad repository audits and encountered several oversized or misaddressed
queries. Its longer observed time is not a controlled estimate of the treatment.

### E317Q: the same supported annotation from either route

The frozen scenario asked whether a researcher should extend the coarse
database note “reduces activity 10000-fold” to a uniform loss-of-function and
cross-assay inactivity label. That extension was an explicitly synthetic
curation proposal, not an observed scientist's decision.

Both answers revised it. Both retained the unequal author-reported mandelate
`kcat` reductions (4,500-fold for R and 29,000-fold for S), bromide-elimination
nondetection without a stated detection limit, and irreversible inactivation by
racemic alpha-phenylglycidate described as comparable to WT. Inactivation
susceptibility is a separate endpoint, not a turnover measurement or an
identified adduct. Both bounded the no-conformational-alteration report to the
2.1 Å inhibitor-bound E317Q context; it does not establish productive chemistry
or assay-general inactivity.

The source-only answer's optional general-acid interpretation is explicitly
proposed and source-supported, not a claim that proton transfer was observed.
Atlas more explicitly states the contextual WT comparator and lack of numerical
inactivation equivalence. These clarifications do not change the requested
annotation. Optional isotope-effect and `kcat/Km` details do not decide the task.

Both routes received the same exact indexed abstract from an
[archived PubMed capture](https://pubmed.ncbi.nlm.nih.gov/7893689/), with
bibliographic, scope and typography fields only. Atlas interpretation fields
were omitted from the common packet. This is archived tool-extracted abstract
text, not retained raw HTTP, full methods or publisher full text. The existing
[recovery record](../../data/atlas/study_context/mandelate_1995_e317q/source_recovery.json)
binds the original local witness; no new source was acquired.

The routes switched roles from the ThDP task, used an eight-minute ceiling and
a 350-word scientific-answer scope. Both disclosed the broad revise conclusion
before inspection. Exact paths were supplied to both, so this was assisted
retrieval, not an unassisted usability test. The Atlas entry point was:

```sh
python scripts/query_atlas_perturbations.py --comparison mandelate_1995_e317q:E317Q:chemical-endpoint-context
```

Atlas ran that query three times because the full and broad-filtered outputs
were truncated before a targeted selection succeeded. Existing context, model
similarity and output handling still limit any performance interpretation.

## What this changes

Keep the supported records and capabilities, but stop automatic case expansion
on the strength of these results. The defensible incremental finding is one
material curation qualification, with no changed broad decision or demonstrated
work reduction in either task. There was no researcher evaluation, held-out
generalization test, project experiment or enzyme-design result.

The new raw-stereo query adapter in [PR #124](https://github.com/VivekVardhanArrabelli/catalytic-earth/pull/124)
was merged and verified in two exposed development contexts, M0213 and M0066.
**Neither usefulness comparison needed that change.** They evaluate older Atlas
capabilities, so they cannot establish the new adapter's practical utility.
Evaluation could have preceded today's implementation. This is a priority
correction, not a reason to build another interface or expand the case count.

The next justified work must name a consequential question where combining
existing evidence across contexts could alter an answer or remove substantial
source-assembly work, with an accessible comparison and a stopping condition.
Test that proposition before adding code or sources; stopping remains valid.
An internal comparison is allowed without inventing a new human-review gate.
Actual researcher impact and prospective experimental performance require their
own evidence and cannot be supplied by more agents.

## Retained audit material

The chronological protocol, exact common-packet hashes, exposure disclosures,
full locked answers, reference/adjudication outputs and app timing metadata are
retained locally under Git-common `catalytic-earth-runs/`:

- `20260922T134756Z-reuse-sprint.md`: selection, freeze and publication receipt.
- `20260922T145303Z-checks/thdp-*.md`: locked ThDP answers and judgments.
- `20260922T145303Z-checks/e317q-*.md`: locked E317Q answers and judgments.
- `20260922T145303Z-checks/e317q-common-primary-packet.json`:
  3,496 bytes; SHA256 `e1ea1ef522ed0e30199368387c673c55c073455aa66fe1817d5bf3f81623b6d2`.

The raw abstract and local agent transcripts are not redistributed with this
brief. All cases remain exposed development material. No scientific review
state, protected registry, source allowance or prior claim is promoted by this
evaluation.
