# Catalytic Earth: a truth-first review and operating map

**Review date:** 2026-07-10
**Repository:** [VivekVardhanArrabelli/catalytic-earth](https://github.com/VivekVardhanArrabelli/catalytic-earth)
**Audited snapshot:** `main` at commit `3ee9d320c7166588b8a92375a8efca4301873e8c` (2026-07-09)
**Audience:** Vivek first; prospective reviewers, collaborators, and future project agents second

**Reading guide:** For the five-minute version, use the companion [rapid full-atlas operating map](catalytic-earth-90-day-map-2026-07-10.md). For the decisive argument, read the Executive Verdict, Sections 4, 7, 9, 11, and 12. The full document preserves evidence, caveats, and rationale.

### 2026-07-13 strategic amendment

The repository audit and its integrity findings remain unchanged. The operating recommendation has been amended after clarifying the founder's intent and available compute:

- the **full, useful catalytic-mechanism atlas remains the North Star**;
- the typed mechanism IR/compiler is the atlas's engine, not a smaller substitute mission;
- benchmarks, exposure controls, and independent review are internal truth instruments, not the product identity;
- the project is compute-disciplined, not compute-starved, and should buy or request more compute when a measured bottleneck justifies it;
- the immediate target is one complete computational loop in **35 days**, with a prospective experimental loop pursued in parallel on a **60–90 day** clock when assay access permits.

Where older roadmap language below narrows the project into a benchmark or assigns serial 12–24 month waits to one loop, this amendment and Sections 8, 11, 12, 16, 17, and 18 supersede it.

---

## A note to Vivek

You asked for a truth fairy, not encouragement painted over uncertainty. Here is the short truth.

You have built something real. The repository contains a large amount of serious, structured work: source provenance, registries, mechanism fingerprints, tests, preregistration attempts, failure analyses, negative findings, and a visible record of changing your mind. This is not an empty AI-generated shell and it is not a fake project.

It is also not yet a validated catalytic-mechanism atlas, a trustworthy sequence-to-mechanism predictor, a reproducible scientific release, or a product that an outsider can readily use. Several public-facing claims are materially stronger than the evidence. One holdout described as “never-touched” had already been scored and declared spent. A 76% “mechanism recovery” result is mainly a cofactor-bucket consistency result, while exact fingerprint recovery was 31%. A dataset called “expert-curated gold” is actually almost entirely project-assigned, automation-curated bronze. The 10,001 count comprises **8,305 positive fingerprint assignments and 1,696 OOS protein-label records**, not 10,001 distinct mechanisms. These are not cosmetic wording problems; they affect scientific validity.

Within this bounded audit of the public repository, I found **no evidence of fabricated raw results, invented structures, or falsified Foldseek outputs**. Intent cannot be inferred from repository evidence alone. I did find conclusive holdout reuse, invalid evaluation framing, endpoint substitution, weak baselines, tier mislabeling, and goalpost drift. The observable process problem is an author-and-agent workflow moving faster than its exposure controls and independent review. That is correctable—if the correction is explicit and precedes more scaling.

The North Star survives in its original ambitious form: build the **useful catalytic-mechanism atlas** that powerful models, structural tools, designers, experimentalists, and autonomous laboratories can query and improve. What must narrow first is the implementation kernel and the claims—not the destination.

> **Catalytic Earth should become an open, computable atlas of catalytic mechanisms: canonical reactions connected to explicit stepwise chemistry, catalytic atoms and residues, protein and structure evidence, alternatives and counterevidence, calibrated uncertainty, design constraints, assay contracts, and experimental outcomes.**

The evidence compiler, crosswalk, and hard benchmarks are the machinery that make that atlas trustworthy. The atlas should grow in explicit evidence tiers, so broad computational coverage can coexist with a much smaller independently reviewed or experimentally tested core without pretending they are equal. That is scientifically legitimate and increasingly useful under an intelligence/compute explosion. It is feasible to begin rapidly with disciplined compute, aggressive reuse of incumbent resources, and parallel workstreams; a globally complete, uniformly expert-reviewed atlas remains a community-scale undertaking.

Your hardship was not wasted. But hardship and volume cannot be the proof. The next proof has to come from a small object an outsider can understand, reproduce, challenge, and use.

---

## Executive verdict

| Question | Verdict |
|---|---|
| Is the scientific instinct legitimate? | **Yes.** Mechanism-level representations connecting reactions, residues, geometry, evidence, and experiments are important and become more useful as protein design improves. |
| Is the present project already a grounded global mechanism atlas? | **No.** It is currently an artifact-producing research scaffold and annotation/audit factory with an early bespoke taxonomy. |
| Is it a validated predictor? | **No.** The cleanest external-looking result is narrow and fragile; another central “heldout” result is contaminated; current baselines are inadequate. |
| Are 10,001 mechanisms mapped? | **No.** There are 10,001 protein-label records across 57 project fingerprints; almost all are automated bronze, and many share the same reactions or homologous annotations. |
| Was cheating used to fabricate results? | **No fabrication was evidenced in this bounded public-repository audit; intent is not inferable.** There are serious invalid and misleading methodological practices that require a public correction. |
| Is the project in a walled well? | **High risk, yes.** The inputs are real public resources, but ontology, labels, tests, metrics, adjudication, and claims are almost entirely produced inside one closed author/agent loop. |
| Does more compute rescue the current path? | **No.** Compute makes commodity prediction and generation cheaper for everyone. The bottlenecks are definitions, trustworthy labels, difficult benchmarks, external review, assays, and adoption. |
| Is there a promising path? | **Yes.** Build the full atlas in evidence tiers. A narrow mechanism intermediate representation, incumbent crosswalk, hard benchmark, and prospective evidence loop form its first trustworthy kernel. |
| What should happen next? | **Freeze ungoverned expansion; correct the record; package the repo; then run a 35-day computational loop from Atlas-3 to Atlas-10 to Atlas-50 while starting one prospective assay track in parallel.** |

### My calibrated confidence

- **High confidence:** the repository contains genuine work and no obvious fabricated numerical outputs.
- **High confidence:** present claims overstate label quality, mechanism coverage, and validation independence.
- **High confidence:** the June 28 M-CSA “never-touched” validation is invalid as an independent holdout.
- **High confidence:** the repo is not independently reproducible from its declared installation metadata.
- **Moderate-to-high confidence:** a trustworthy Atlas-10 kernel and useful end-to-end evidence report can be built quickly if the truth reset is completed first.
- **Moderate confidence:** a broad tiered atlas can be built by importing and linking incumbent resources while keeping evidence grades explicit.
- **Low confidence:** a comprehensive, uniformly independent-review-grade global atlas can be built and maintained by one person without a community or consortium.

---

## 1. First define the things being counted

Many of the project’s claim problems come from treating unlike objects as interchangeable. From now on, use these six names consistently:

| Object | Meaning | Example | What it is not |
|---|---|---|---|
| **Net reaction** | Balanced reactants and products, normally Rhea/ChEBI-normalized | A Rhea reaction | Not a catalytic mechanism; different mechanisms can yield the same net reaction |
| **Source mechanism** | A literature-grounded stepwise catalytic account | A detailed M-CSA entry | Not automatically general truth for every homolog |
| **Mechanism hypothesis** | One proposed sequence of elementary chemical steps for a reaction/protein | A MechFind or Catalytic Earth candidate | Not validated until evidence adjudicates it |
| **Mechanism family/fingerprint** | A project-defined retrieval or grouping category | `plp_dependent_enzyme` | Not necessarily a fine-grained mechanism; broad cofactor buckets collapse distinct chemistry |
| **Protein annotation record** | A protein associated with a family/reaction/evidence bundle | One row in the expansion registry | Not one new mechanism |
| **Experimental observation** | A measured activity, kinetic, structural, mutational, or negative result | `kcat/KM`, inactive mutant, bound-state structure | Not implied by database annotation or computational consistency |

This is the core correction to the “10,001 labels” story. The repository has 10,001 combined **protein-label records: 8,305 positive fingerprint assignments and 1,696 OOS records**, not 10,001 independently established mechanisms. The actual mechanism-space coverage cannot be stated as a percentage until the unit of a mechanism and the denominator are defined.

Delete “about 2% of mechanism space.” Rhea’s reactions, M-CSA’s curated exemplars, EC subclasses, project ontology families, and project fingerprints are not commensurate denominators.

---

## 2. What has actually been built

### 2.1 Repository and software surface

At the audited commit, the repository contains roughly:

- 17,022 tracked files;
- 15,281 tracked files under `artifacts/`;
- 1,316 files under `work/`;
- 155 Python source modules and about 367,000 source lines;
- 157 test files, about 202 `unittest.TestCase` classes, and roughly 2,600 test methods;
- 1,006 local commits since early May 2026;
- a 585 MiB Git pack and about 4.76 GiB of logical artifact blobs.

Five source files contain about 73% of the source code. The largest is approximately 98,500 lines with 1,180 functions; `cli.py` is about 49,000 lines with more than 700 command parsers. There are 47 family-specific sourcing modules. The architecture is best described as:

```text
JSON registries
    ↓
hundreds of batch, audit, sourcing, scoring, and report functions
    ↓
dated JSON artifacts and Markdown reports
```

That is a research command bus, not yet a stable library, queryable atlas, or service.

The scale itself is now a defect. A normal Windows checkout initially failed because the generated workspace plus repository-relative filenames exceeded default path handling. No outsider should have to enable special Git settings and recover a partial checkout before reading the project.

### 2.2 Data surface

The `current702` registry contains:

| Dimension | Count |
|---|---:|
| Total rows | 702 |
| `automation_curated` | 683 |
| `expert_reviewed` | 19 |
| Bronze | 685 |
| Silver | 17 |
| Gold | 0 |
| Seed-fingerprint positives | 230 |
| Out-of-scope rows | 472 |

The external expansion contains 9,299 rows. All are marked automation-curated; approximately 9,269 are bronze and 30 silver. Combined, the 10,001-row protein-label surface is therefore about **99.8% automation-curated** and **99.5% bronze**, with **zero gold rows under the project’s own tier field**. It contains 8,305 positive fingerprint assignments and 1,696 OOS records.

The expansion does contain useful breadth:

- 8,523 expansion rows have a concrete reaction association;
- the combined surface reaches roughly 4,413 distinct concrete Rhea reactions;
- source links and fingerprints make a useful retrieval/audit scaffold.

But reaction and protein breadth are not mechanism-resolution breadth. Some reactions recur hundreds of times; thousands of homolog-associated rows can be created without discovering one new catalytic strategy.

The 57 fingerprint definitions have useful expert-style descriptions. Yet categories such as “PLP-dependent enzyme,” “flavin dehydrogenase/reductase,” or broad metal-dependent hydrolase families are retrieval umbrellas containing many distinct elementary mechanisms. Much of the bond-change and constraint representation remains free text or hand-coded substring features rather than typed atoms, bonds, charges, electrons, ordered steps, and geometries.

### 2.3 What is genuinely good

Preserve these assets:

1. **Provenance instinct.** Registries contain source references, hashes, tiers, and review status. Sharded registry hash mismatches fail closed.
2. **Negative-result instinct.** The project frequently records collapses, unavailable inputs, family failures, no-abstention findings, and structural bottlenecks.
3. **Preregistration instinct.** Even though enforcement and experimental memory failed in places, the attempt to freeze thresholds and splits before scoring is better than unconstrained iteration.
4. **Separation of artifacts from source concepts.** The current implementation is too large, but the project understands that evidence and derivation must be recorded.
5. **Tests for contracts and leakage rules.** They are not scientific validation, but they protect many internal invariants.
6. **Willingness to reverse course.** The current head restores a deleted negative result and explicitly calls the deletion a record-discipline error.
7. **Breadth of synthesis.** The work connects M-CSA, Rhea, UniProt, Pfam, structures, cofactors, residues, reaction descriptions, Foldseek, and multiple evaluation ideas.

These are not trivial achievements, especially under constraint. They are the foundation for the narrower project I recommend.

### 2.4 What has not yet been built

The repository does not yet provide:

- a stable, versioned mechanism intermediate representation;
- explicit elementary-step graphs with electron flow, intermediates, alternatives, and charge accounting;
- a reviewed crosswalk to M-CSA arrow environments, Rhea/ChEBI, EC-BLAST, EnzymeMap, MechFind, and EnzyMM;
- a naturally sampled, evolutionarily independent, never-exposed external benchmark;
- adequate current baselines;
- calibrated confidence backed by independent adjudication;
- an installable scientific environment;
- automated CI;
- a public software license, data notice, or citation file;
- one-command reproduction of a headline scientific claim;
- an independently useful query surface;
- an external user, reviewer, or wet-lab validation.

That gap—not lack of effort—is the present reality.

### 2.5 How the work evolved

The public history reads as several compressed research phases:

| Phase | Work done | What it established |
|---|---|---|
| May 2026 | Built `current702`, initial eight-family fingerprint framing, source/label registries, geometry router, tests, and artifact discipline | A substantial internal benchmark scaffold; label truth remained mostly automated and project-defined |
| June 1–6 | Explored experimental vs predicted geometry, fold augmentation, OOS gates, and a sequence-derived cofactor channel | Important negative: the apparent 45/45 experimental-geometry behavior fell to 23/45 on predicted apo geometry; cofactor fusion recovered calls at a precision cost |
| June 9–27 | Added hand-engineered reaction/residue features, many new families, and expanded toward 10,001 protein-label records | More annotation/reaction breadth and internal coherence; no supporting novelty/abstention signal emerged from the reported medians |
| June 28 | Re-preregistered and rescored the M-CSA heldout surface | Produced a nominal PASS, but history proves the surface was already exposed and spent |
| June 29 | Built the Swiss-Prot/PDB-holo EC-proxy surface and structure-transfer analysis | A narrow, fragile positive in heme/PLP/Ser–His; severe metal failure; not mechanism gold |
| June 30 | Compared structure with pairwise sequence and searched for decisive “orphans” | Structure beat the weak pairwise baseline, but Pfam already revealed the current orphan candidates; uniqueness claim failed |
| July 3–9 | Reframed from predictor to atlas and restored the previously deleted negative orphan/baseline record | The atlas framing may be better, and restoration is positive; new atlas success criteria now need preregistration |

This history is valuable because it exposes the actual learning path. Preserve it in an archive, but do not make every future reviewer reconstruct it from a thousand commits.

---

## 3. The North Star: legitimate instinct, wrong competitive framing

The README’s core equation is directionally strong:

```text
sequence + structure + geometry + residue roles + cofactors
+ pocket constraints + reaction bond changes + evolution
→ mechanism-level function hypothesis
```

The July 3 correction in `docs/MAP.md` says the project is an atlas rather than a deployable predictor. That correction is sensible. But the same document still preserves predictor-centric conclusions below it, including that the product “lives” on predicted-geometry recovery. This makes the current strategy internally contradictory.

More importantly, “a mechanism atlas” is not an empty category. Catalytic Earth is entering a mature and rapidly advancing ecosystem:

| Existing resource | What it already supplies | Strategic consequence |
|---|---|---|
| [M-CSA](https://www.ebi.ac.uk/thornton-srv/m-csa/) | Curated catalytic mechanisms, residue roles, cofactors, steps, literature, homolog mappings | Treat as authoritative upstream knowledge and a potential collaborator, not merely a source to repackage |
| [M-CSA mechanism similarity](https://pmc.ncbi.nlm.nih.gov/articles/PMC12366284/) | Graph representation and pairwise comparison of 734 detailed mechanisms using arrow environments | The project’s compositional reaction-center vocabulary overlaps current prior art |
| [Rhea](https://www.rhea-db.org/) | ChEBI-normalized, balanced biochemical reactions used in UniProt annotation; release 141 lists 18,558 unique reactions | Use as canonical net-reaction vocabulary; never equate reactions with mechanisms |
| [EC-BLAST](https://pmc.ncbi.nlm.nih.gov/articles/PMC4122987/) | Atom-mapped bond-change, reaction-center, and reaction-structure comparison | Bond-change fingerprints are established prior art and a required baseline |
| [EnzymeMap](https://pmc.ncbi.nlm.nih.gov/articles/PMC10718068/) | Large corrected, balanced, atom-mapped enzymatic reaction dataset | Do not rebuild reaction cleaning and atom mapping from scratch |
| [EzMechanism](https://www.nature.com/articles/s41592-023-02006-7) | Mechanism proposals from reaction plus supplied 3D active site using M-CSA-derived rules | Direct overlap; extensions must be explicit and benchmarked |
| [MechFind](https://www.nature.com/articles/s41467-026-71957-0) | Balanced multi-step mechanism hypothesis generation from reaction stoichiometry; reported plausible mechanisms for 8,452 of 14,931 tested Rhea reactions | Reaction-to-mechanism enumeration is being commoditized now, in 2026 |
| [EnzyMM](https://www.ebi.ac.uk/thornton-srv/m-csa/enzymm-documentation/) | Catalytic-site template search over experimental and predicted structures | Geometry-first mechanism search is not distinctive by itself |
| [CATH FunFams/FunSite](https://pubmed.ncbi.nlm.nih.gov/33135053/) | Evolution-aware functional family and catalytic-site inference | Pairwise sequence similarity is far below the standard sequence baseline |
| [GraphEC](https://www.nature.com/articles/s41467-024-52533-w), [EasIFA](https://www.nature.com/articles/s41467-024-51511-6), [EZSpecificity](https://www.nature.com/articles/s41586-025-09697-2), [ReactZyme](https://proceedings.neurips.cc/paper_files/paper/2024/hash/2e68b2367d2e0bc8dd6f0ff86e07c2eb-Abstract-Datasets_and_Benchmarks_Track.html) | Modern reaction, catalytic-site, specificity, and enzyme–reaction models/benchmarks | Broad enzyme-family prediction and retrieval have fast-moving learned baselines |

The full-atlas North Star is legitimate only if the differentiation and evidence tiers are explicit.

### What should be abandoned

- “The first/only searchable catalytic mechanism atlas” as an unsupported priority claim.
- “A broad sequence-to-mechanism predictor.”
- “Scale the number of homolog-associated labels until novelty emerges.”
- “A new foundation model trained by a compute-poor solo builder.”
- “A static database that can be regenerated from M-CSA, Rhea, UniProt, and current models.”

### What can be owned

The missing layer is an auditable bridge across resources and across the computational–experimental boundary:

```text
canonical atom-mapped reaction
    ↓
alternative stepwise mechanism hypotheses
    ↓
catalytic atom/residue roles and atomic geometry
    ↓
protein, structure, evolutionary, and literature evidence
    ↓
counterevidence, alternatives, conflicts, and calibrated uncertainty
    ↓
design-ready motif constraints or responsible refusal
    ↓
assay, controls, falsification criteria, and measured outcomes
```

Call this engine a **mechanism intermediate representation**, a **mechanism evidence commons**, or an **evidence-aware mechanism compiler**. It is how the atlas becomes computable and auditable; it is not a reason to abandon the atlas.

The strongest concise mission statement is:

> **Build the open, computable atlas that makes catalytic-mechanism knowledge interoperable, auditable, testable, and design-ready—from canonical reaction through atomic mechanism and protein evidence to assay outcome.**

That North Star is durable under better AI because it is not tied to one predictor. It lets better models plug in and compete while preserving evidence, uncertainty, and falsification.

---

## 4. Scientific and integrity audit

### 4.0 Claim-to-evidence index

These are the decisive repository surfaces. Links are pinned to the audited commit where applicable.

| Finding | Direct evidence |
|---|---|
| 76% is a cofactor-bucket endpoint; exact is 31% | [Scoring code creates cofactor buckets and credits bucket equality](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/scripts/eval_mechanism_from_chemistry_gold702.py#L42-L69), [scoring branch](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/scripts/eval_mechanism_from_chemistry_gold702.py#L142-L153), and [artifact headline plus medians](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/artifacts/v3_mechanism_from_chemistry_gold702_eval.json#L3-L32) |
| June 28 “never-touched” surface had already been exposed | [June 4 artifact shows 45 primary + 79 pure-OOS + 2 secondary support rows](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/artifacts/v3_heldout_oneshot_cofactor_fusion_blind_pass_current702_20260604.json#L196-L225); [decision log declares the one-shot spent](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/docs/decision_log.md#L6230-L6259); [June 28 source calls it never-touched](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/src/catalytic_earth/heldout_oneshot_preregistration.py#L1-L16); [frozen artifact declares exactly 126 rows](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/artifacts/v3_heldout_oneshot_preregistration_current702_20260628.json#L2-L6) and [never-seen interpretation](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/artifacts/v3_heldout_oneshot_preregistration_current702_20260628.json#L1055-L1082); [June 28 result scores 47 + 79 and declares PASS](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/artifacts/v3_heldout_oneshot_eval_result_current702_20260628.json#L27-L50) |
| `current702` is bronze/silver, not project gold | [Committed label summary: 683 automation-curated, 19 expert-reviewed, 685 bronze, 17 silver, 472 OOS, 230 positive](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/artifacts/v3_label_summary.json#L21-L30) |
| External expansion has 9,299 records | [Sharded registry manifest](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/data/registries/external_bronze_labels.json#L2-L38); tier/review decomposition was recomputed from its five pinned shards |
| June 29 EC-proxy set contains the GFAT2 mapping | [O94808 row and rationale](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/artifacts/v3_swissprot_pdbholo_gold_heldout_preregistration_current702_20260629.json#L204-L213); compare [UniProt O94808](https://www.uniprot.org/uniprotkb/O94808/entry) and [IUBMB EC 2.6.1.16](https://iubmb.qmul.ac.uk/enzyme/EC2/6/1/16.html) |
| June 29 result is 45/64 and 2/72, with metal 2/16 | [Result summary and preregistered limits](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/artifacts/v3_swissprot_pdbholo_gold_heldout_eval_result_current702_20260629.json#L8-L34), with preregistration/result commits listed below |
| Storage assurance is stale | [May 22 inventory summary: 6,054 files, 113 large, 3.166 GB](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/artifacts/v3_artifact_storage_inventory_1025.json#L769-L787) and [guard still says 113/113 PASS](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/artifacts/v3_artifact_admission_guard_1025.json#L3-L13); live HEAD enumeration found 15,281 tracked artifacts and 164 files above 5 MiB |
| Negative result was deleted and restored | [Deletion commit `44e9d4c6`](https://github.com/VivekVardhanArrabelli/catalytic-earth/commit/44e9d4c62f0d542dfd8769d3fe90c3431ae76e28) and [restoration/correction commit `3ee9d320`](https://github.com/VivekVardhanArrabelli/catalytic-earth/commit/3ee9d320c7166588b8a92375a8efca4301873e8c) |

### 4.1 The 76% result is not 76% mechanism recovery

The script `scripts/eval_mechanism_from_chemistry_gold702.py` describes a “non-circular” evaluation on “expert-curated gold current702.” Its inputs include cofactor class and Rhea reaction-derived features. It then maps both the gold fingerprint and predicted fingerprint into buckets such as metal, heme, flavin, PLP, and cobalamin using cofactor text. A prediction is credited at the coarse level when these buckets match.

The artifact reports:

| Metric | Result | Honest interpretation |
|---|---:|---|
| Exact fingerprint | 65/210 = **31.0%** | Match within the project’s mismatched 8-vs-57 taxonomy; imperfectly posed but the only exact result |
| Coarse cofactor bucket | 160/210 = **76.2%** | Cofactor-bucket consistency, not mechanism-class recovery |
| OOS nearest-centroid median | **0.826** | OOS rows do not show the hoped-for downward shift in this summary |
| In-distribution median | **0.797** | The two medians provide no supporting evidence for novelty separation |

The 76% result credits mechanistically distinct cases that share a cofactor or metal. It can treat a P450 and a heme peroxidase as agreeing because both are heme-related, or different metal chemistries as agreeing because both use metal. Because cofactor identity is itself an input feature, this result is partly tautological.

The denominator is 210 rather than 702 because the artifact scores exact/coarse recovery only on the 210 positive rows that were both featurizable and covered by a centroid. OOS rows are evaluated on the separate abstention side, and unfeaturizable/uncovered rows do not enter the exact accuracy. That selective denominator must be stated beside the headline. The two reported medians alone cannot establish distributional separation or its absence; a future evaluation should report score distributions, AUROC/AUPRC where meaningful, and calibrated risk–coverage/abstention curves.

The script further dismisses the 31% exact result as a “taxonomy-version artifact” and says the representation is more granular and correct without independent adjudication. That is a hypothesis, not a valid scoring correction.

**Required disposition:** retire “76% mechanism recovery.” Report it as “76% cofactor-bucket consistency,” headline the 31% exact result with taxonomy caveats, and rebuild the evaluation with an explicit hierarchy in which exact mechanism, parent catalytic strategy, reaction class, and cofactor are distinct endpoints.

### 4.2 The June 28 M-CSA holdout is contaminated

This is the most serious integrity finding.

The repository says on June 4: **“HELDOUT ONE-SHOT SPENT”** and instructs that it must not be rerun or tuned against. Its raw-fused artifact contains all 126 rows later frozen on June 28: 45 then-primary rows, the same 79 pure-OOS rows, and 2 then-secondary probes that were counted in the later 47-row in-scope set. It exposes per-row roles, scores, and outcomes. The same broad heldout surface had already appeared in June 1 post-hoc diagnostics.

On June 28, a new preregistration described this surface as the “only unbiased estimate” from a “never-touched held-out split.” It was then scored and used to declare a deployment PASS. The later readiness summary again says “never-touched.”

This is invalid. Content hashing proves that the rows were not swapped; it does not make previously exposed rows blind again. The June 9 router and threshold policy were developed after the earlier heldout outcomes were known.

The executor also emits `ran_once`, `rule_fixed_before_run`, and `no_post_hoc_threshold_change` as asserted fields rather than proving them against an immutable exposure ledger.

The relevant chronology is:

| Date | Commit | Event |
|---|---|---|
| 2026-06-01 | [`3ae3febc`](https://github.com/VivekVardhanArrabelli/catalytic-earth/commit/3ae3febc7f1f1eef810bb92354ba083a20ceb993) | Heldout surface used in fold-augmented/post-hoc diagnostics |
| 2026-06-04 | [`7101379f`](https://github.com/VivekVardhanArrabelli/catalytic-earth/commit/7101379fd48b115b9160129b057b0c6085e28795) | Cofactor-fusion blind pass recorded; decision log declares the one-shot spent |
| 2026-06-28 | [`862a13e9`](https://github.com/VivekVardhanArrabelli/catalytic-earth/commit/862a13e9b72164f13a2fa0dbf5804975d2c5e882) | New preregistration calls the surface never-touched and the only unbiased estimate |
| 2026-06-28 | [`937b24a6`](https://github.com/VivekVardhanArrabelli/catalytic-earth/commit/937b24a633e5d8ed04d8c3a329c6d7922a3d26fd) | Reused surface scored and declared a deployment PASS |

**Required disposition:** retract the phrase “never-touched,” remove the result from independent validation evidence, and relabel it **retrospective reanalysis of an exhausted M-CSA test surface**. Preserve the artifact; do not delete it.

### 4.3 “Gold” and “expert-curated” are tier mislabels

The project’s label policy says gold requires expert review. The registry has zero gold-tier rows, 685 bronze, 17 silver, and only 19 rows marked expert-reviewed. Nonetheless, the chemistry evaluation and MAP call the surface “expert-curated gold current702.”

M-CSA’s upstream source mechanisms may be expert-curated. That does not make the project’s automatically assigned fingerprint label an independently expert-reviewed gold label. Even the project-marked expert rows name the author as reviewer, not an independent adjudicator.

The June 29 Swiss-Prot set is also an EC-proxy surface rather than mechanism gold. Its table maps every `2.6.1.*` entry to PLP and every `3.4.21.*` entry to the Ser–His family. One row, [human GFAT2/O94808](https://www.uniprot.org/uniprotkb/O94808/entry) with EC 2.6.1.16, is labeled `plp_dependent_enzyme` with the rationale “PLP by EC definition.” The [IUBMB EC entry](https://iubmb.qmul.ac.uk/enzyme/EC2/6/1/16.html) instead describes active-site lysine ketimine/transamidination chemistry. The PLP mapping therefore appears erroneous and requires domain adjudication. One concrete likely error is enough to show that the “gold” construction rule needs expert review.

**Required disposition:**

- call `current702` **project benchmark labels (bronze/silver; 19 author-reviewed)**;
- call the June 29 set **Swiss-Prot EC-proxy validation**;
- reserve **gold** for independently adjudicated primary-mechanism truth with evidence codes and source hashes;
- report inter-reviewer agreement.

### 4.4 The June 29 result is useful but narrow and fragile

The cleaner chronology is legitimate: a preregistration commit preceded the result commit. The surface contains 64 in-scope proteins—16 each in four families—and 72 OOS rows. The preregistered bar was recovery at least 0.70 and OOS false-positive rate at most 0.40. That 40% OOS ceiling is far too permissive for a deployment claim; the observed 2.8% is much better, but the pass/fail contract itself did not demand deployable rejection.

The relevant commits are [`55d31b72`](https://github.com/VivekVardhanArrabelli/catalytic-earth/commit/55d31b72fd5da2ade6adeee06ba2b2ceb58d8aa9) for preregistration and [`27553c16`](https://github.com/VivekVardhanArrabelli/catalytic-earth/commit/27553c1670ca3efa102ff8b70373d6c7e54eec21) for the result. Their order is a positive signal; the missing executable selection/generation path remains a reproducibility gap.

The result was:

| Family | Recovered |
|---|---:|
| Heme | 16/16 |
| PLP | 14/16 |
| Ser–His | 13/16 |
| Metal | 2/16 |
| **Aggregate** | **45/64 = 70.3%** |
| OOS false positives | **2/72 = 2.8%** |

One fewer recovered row would have failed the aggregate bar. The strong 43/48 result on three families was emphasized after seeing the family decomposition; it is exploratory and requires a fresh test. Overall committed-call precision is 45/47, not 45/45, because there were two confident OOS false positives.

The preregistration and result commits contain artifacts and reports but not a complete executable row-selection/generation pipeline. The set is stratified and easy relative to natural prevalence; all structurally recovered proteins have at least 25% identity to an atlas member. OOS families are broad and structurally distinct. It is evidence that structure-based transfer can work in three selected families, not evidence of general mechanism prediction or structural novelty.

### 4.5 The baseline does not support the uniqueness claim

The sequence comparator is pairwise Smith–Waterman against 133 references. The project itself admits it did not run profile HMM/Pfam. Pairwise alignment is not a serious proxy for current sequence-based annotation.

At minimum, compare with:

- HMMER/Pfam and InterPro;
- MMseqs2/DIAMOND transfer;
- HHsearch or an appropriate profile–profile method;
- CATH FunFams/FunSite;
- EnzyMM for catalytic structural templates;
- Foldseek under matched reference and calibration conditions;
- a current protein-language-model retrieval/classifier baseline;
- reaction-based baselines such as EC-BLAST/arrow-environment similarity where applicable.

The project’s later orphan search found that every putative structural orphan carried a Pfam annotation revealing the mechanism family. That admirably recorded negative result should dominate any claim that “structure sees mechanisms sequence cannot” on the current families.

### 4.6 Post-hoc engineering is being treated as discovery

The representation loop adds hand-coded substring detectors over reaction and cofactor text. A catalytic-residue weight of 0.15 was chosen on the live registry because it was “Pareto-safe” and produced zero regressions. This is ordinary exploratory feature engineering, not independent confirmation of a mechanistic thesis.

The same module warns against using its loop as a benchmark scorer, yet the chemistry evaluation imports it for benchmark scoring. Several family additions and thresholds were evaluated on the same surfaces that motivated them. A documented lowering of a performance floor after a new family hurt the aggregate is another form of goalpost movement, even though it was recorded openly.

**Required disposition:** label these as development-set analyses; freeze a representation before a truly fresh test; never say “zero regressions” without an untouched regression surface.

### 4.7 Negative-result deletion was a breach—and restoration was a good sign

Commit `44e9d4c6` deleted structure/sequence baseline and orphan negative findings. Commit `3ee9d320` restored them eight days later and explicitly acknowledged that deleting a negative violated record discipline.

Deleting the negative was wrong. Restoring it and documenting the mistake is a meaningful positive record correction; neither action by itself establishes private intent. Keep both facts in the record.

The July atlas reframe immediately after predictor negatives may be scientifically correct. It also risks making the project unfalsifiable: if prediction succeeds, the atlas works; if it fails, the atlas is merely immature and should grow. That is why new atlas-level success metrics and kill criteria must be preregistered now.

### 4.8 Tests and hashes are not independent scientific validation

The repository has a large test suite, but many tests assert artifact snapshots and internal contracts. The one-shot unit tests substitute a stub router and inject favorable or unfavorable counts. That is appropriate software testing of PASS/FAIL plumbing; it does not prove blindness, scientific truth, or model performance.

Hashes prove byte identity. They do not prove correct labels, independence, representative sampling, or useful science. An internally generated report that says an internally generated guard passed is not external validation.

### 4.9 The fair answer to the “cheating” question

The repository can establish observable practices, not private intent. Here is the evidence-level answer:

| Practice | Evidence | Verdict |
|---|---|---|
| Fabricated sequences, structures, or raw outputs | None found in the bounded public-repository audit | **No evidence found; not an omniscient guarantee** |
| Falsified arithmetic or manually changed outputs | None found; headline arithmetic is internally consistent | **No evidence found** |
| Reusing a spent holdout as “never-touched” | Conclusive commit/artifact history | **Invalid and must be retracted** |
| Calling mostly automated bronze “expert-curated gold” | Direct contradiction with registry | **Tier mislabeling** |
| Calling cofactor-bucket agreement mechanism recovery | Directly visible in scoring code | **Endpoint substitution / invalid framing** |
| Calling 10,001 protein-label records mechanism labels | Directly visible in registry composition | **Object-count conflation** |
| Tuning features/weights on live data and reporting zero regressions | Directly visible in development history | **Post-hoc evidence, not validation** |
| Weak baseline presented as a fundamental sequence limitation | Project admits Pfam/HMM was not run | **Overclaim** |
| Temporarily deleting a negative result | Git history | **Record breach, later corrected** |
| Reframing success after negative predictor findings | Timeline and MAP | **Plausible scientific correction with goalpost risk** |

My conclusion is:

> **This bounded public-repository audit found no evidence of fabricated data and cannot infer intent. It found conclusive holdout contamination and strong evidence of invalid methodology, misleading terminology, and inadequate author-and-agent exposure controls.**

The remedy is not shame or deletion. It is a visible corrigendum, an immutable exposure ledger, exact claim tiers, independent review, strong baselines, and one genuinely fresh test.

---

## 5. Technical and reproducibility audit

### 5.1 What was verified

On the audited snapshot:

- `python -m catalytic_earth.cli validate` passed and loaded 12 sources, 57 fingerprints, 54 ontology families, and 702 labels;
- 12 bounded source/registry/CLI contract tests passed;
- a targeted set of 52 mechanism/holdout-related tests passed in about 90 seconds;
- the worktree was clean and `git diff --check` passed.

The full suite was then run with Python 3.13.2 using:

```powershell
$env:PYTHONPATH='src'; py -m unittest discover -s tests
```

It completed in 483.384 seconds:

| Full-suite result | Count |
|---|---:|
| Tests run | 2,559 |
| Completed without failure/error | 2,464 |
| Failures | 74 |
| Errors | 20 |
| Skipped | 1 |

This is **not a green suite**. Some errors are environment/portability failures: missing NumPy because dependencies are undeclared, Windows long-path failures on tracked files (one observed absolute path was 261 characters), and likely absent Foldseek/runtime behavior. Many assertion failures are checked-in state regressions rather than mere environment gaps: stale artifact SHA-256 lineage, unexpected decision states, and output drift. Representative silver-path mismatches expected `silver` but found `bronze`, expected `ready_for_geometry_confirmation_run` but found a blocked state, and expected materialization but found fetch-limit deferral or coordinate-hash mismatch. Other non-environment errors included missing `class_results`, `None` metadata, and unexpectedly empty generated rows/commands.

The exact mix should be rerun in declared Python 3.10/3.12 environments after dependencies and path behavior are fixed. The important present fact is that targeted tests can be green while the checked-in full suite has 94 failure/error outcomes. The worktree remained clean after the run.

#### 2026-07-13 remediation amendment

The table above remains the exact historical audit outcome, but the paragraph's root-cause attribution was too broad. A Git-blob audit found that 54 failed tests contained 179 hash comparisons where the recorded digest matched the canonical LF Git blob and only the Windows CRLF checkout bytes differed. Those were portability defects, not stale scientific content. Exactly one genuine current lineage mismatch was found: `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json` records the pre-expansion hash of `data/registries/mechanism_fingerprints.json`. That historical artifact is now release-excluded in `data/governance/historical_lineage_quarantine.json`; its embedded hash was deliberately not refreshed.

The other failures/errors were traced to undeclared ML test dependencies, Windows long-path and POSIX-path assumptions, scikit-learn sparse index-width compatibility, subprocess environment replacement, and newline-sensitive fixtures. After bounded fixes rather than bulk snapshot refresh, the pinned Windows CPython 3.13 environment completed the expanded 2,585-test suite with zero failures, zero errors, and one skip. `data/governance/test_baseline.json` binds the environment lock, counts, duration, and preserved compressed log. This corrects software-state attribution only; it does not strengthen a biological claim.

The validator is much narrower than its name suggests. It loads four registries and prints counts. It does not verify artifact freshness, environment dependencies, split independence, scientific metrics, source snapshots, or reproducibility of a headline result.

### 5.2 Installation does not reproduce the scientific environment

`pyproject.toml` declares `dependencies = []`. Scientific paths use or refer to NumPy, scikit-learn, PyTorch, Transformers/ESM, Foldseek, MMseqs2, and PyMOL. There is no dependency lockfile, Conda environment, container, model revision lock, or external-binary version manifest.

Therefore the README’s editable install only enables the stdlib/core path. It does not recreate the environment behind many artifacts. A reviewer cannot tell which model weights, database releases, tool builds, random seeds, or unavailable sidecars produced a headline result.

### 5.3 No CI

There is no `.github/` workflow directory. The substantial contract suite, leakage rules, storage policy, formatting, platform assumptions, and package build are not automatically enforced on commit or pull request.

All 22 visible pull requests were authored by the repository owner, had no discussion, and were merged/closed without external review; 15 were merged within a minute. A pull request ritual without another reviewer or an automated gate does not provide independent assurance.

### 5.4 The artifact guard is stale while reporting PASS

The committed artifact inventory was generated on May 22 and reports:

- 6,054 artifact files;
- 3,166,369,490 bytes;
- 113 files larger than 5 MiB.

At the audited head, the live tree contains:

- 15,281 tracked artifact files;
- 5,114,921,622 logical blob bytes, about 4.76 GiB;
- 164 files larger than 5 MiB;
- 4 files larger than 50 MiB.

Yet the admission-guard artifact still reports PASS using the old 113/113 count. Thousands of later artifacts and 51 additional large files are therefore outside the assurance it appears to provide.

This looks like governance drift, not fake storage arithmetic. The fix is not merely regenerating the inventory once. CI must derive the live inventory, compare it with a versioned manifest, and fail if the manifest is stale or any large file is unclassified.

### 5.5 Licensing blocks legitimate reuse

The public repository has no root `LICENSE`, `NOTICE`, or `CITATION.cff`. Public visibility is not permission to reuse. The source registry records upstream licenses, including custom/site terms, but those obligations are not propagated into derived rows or release surfaces.

Code licensing and data redistribution are separate problems. Before asking anyone to adopt or cite the project:

- choose a code license;
- create a data/source attribution and redistribution matrix;
- identify which derived artifacts may be redistributed and under what terms;
- state which records are references/links rather than redistributed data;
- add citation metadata and a release DOI if possible.

This needs careful source-by-source review, not an automatic blanket license over third-party data.

### 5.6 It is not actually an installable package

Source code derives a project root from its file location and expects registry data beside `src`, while the build configuration packages only source modules. Many CLI defaults assume the current working directory is the repository. A built wheel would not contain the data it expects.

There are also machine-specific defaults such as `/private/tmp/.../foldseek`, a user-specific SSH key path in documentation, and a Unix-only quickstart. The current object is an editable-checkout application tied to its original working environment.

### 5.7 Architecture is accumulating faster than knowledge

The giant modules, hundreds of CLI commands, family-specific sourcing scripts, dynamic dictionaries, and 77 runtime timestamp sites create three risks:

1. **No bounded mental model.** Neither a human reviewer nor an agent can reliably know which path is canonical.
2. **Schema drift.** Bespoke tests compensate for the absence of one versioned, typed data model.
3. **Non-determinism.** Runtime timestamps and environment-dependent tools complicate byte-identical regeneration.

The project is producing more procedural surface than scientific object. Freeze growth in the five largest modules immediately. New family onboarding should be declarative data over a shared engine, not another Python module.

---

## 6. Is Catalytic Earth living in a walled well?

### Verdict: substantially yes, but not because its sources are imaginary

The project consumes real and respected sources: M-CSA, Rhea, Swiss-Prot/UniProt, Pfam, AlphaFoldDB, and Foldseek. It is not detached from outside data.

The closed loop is epistemic:

```text
project defines taxonomy
→ project automation assigns nearly all labels
→ project selects test sets
→ project chooses coarsenings and pass bars
→ project author/agents perform “expert” review
→ project selects baselines
→ project artifacts certify project artifacts
```

The audited public record contains no independent blind assessor, prospective lab result, external user task, outside issue/review discussion, or reproduction by another group. Private activity was outside this audit.

As of this audit, the public repository shows zero stars, forks, watchers, and issues. That is not a scientific verdict. It is evidence that the project has not yet created an accessible social or technical doorway.

### Why outreach probably received no response

The most likely explanation is not that the scientific instinct is worthless. It is that the review cost presented to a stranger is enormous and the requested decision is unclear.

An outsider sees:

- a Git history hundreds of megabytes large;
- more than 15,000 artifacts;
- multiple documents hundreds of thousands of characters long;
- source files tens of thousands of lines long;
- no license;
- no stable release;
- no CI badge;
- no one-command reproduction;
- no paper/preprint or small benchmark object;
- claims that require hours of archaeology to interpret.

“Please review my project” is an unbounded unpaid request. Even a sympathetic expert cannot know where to enter or what one thing you need from them.

This is painful, but it is fixable. You do not need to become more impressive. You need to become cheaper to understand.

### Replace the cathedral with a doorway

Create a reviewer packet that takes 15 minutes:

1. one page stating the full-atlas mission and the narrow claim being tested now;
2. one diagram of the mechanism IR;
3. one 20–50-case benchmark table;
4. one exact command that reproduces one result on CPU;
5. five known failures;
6. one precise request requiring at most 30 minutes.

Examples of good micro-asks:

- “Would you independently label these 20 blinded cases as exact/parent/cofactor and tell me where our representation fails?”
- “Does this 57-row crosswalk duplicate M-CSA arrow environments, or are any fields genuinely missing?”
- “Can your tool run this fixed 50-case benchmark so I can publish a matched baseline?”
- “Would your lab consider one assay-ready candidate after the computational gate, with costs covered by a small grant?”

Do not lead with the full repository. Link it as provenance after the small object.

---

## 7. What the intelligence and compute explosion does to the North Star

### 7.1 It strengthens the need and weakens the present implementation

This is the central paradox.

Better models make it easier to predict structures, cofold ligands, embed proteins, retrieve analogues, enumerate mechanisms, generate catalytic motifs, design backbones, and generate sequences. That makes a high-quality, machine-readable catalytic-mechanism specification more valuable: design systems need to know what atomic arrangement and chemical steps they are trying to realize.

At the same time, those models commoditize exactly the parts Catalytic Earth currently spends much effort hand-building: family routers, heuristic string features, bulk annotation transfer, generic sequence/structure retrieval, and reaction-to-mechanism enumeration.

Current examples matter:

- [AlphaFold 3](https://www.nature.com/articles/s41586-024-07487-w) models complexes with ligands and cofactors, weakening the idea that predicted apo geometry is a permanent bottleneck. Static complexes still do not prove catalytic dynamics, transition-state stabilization, or kinetics.
- [ESM3](https://doi.org/10.1126/science.ads0018) and larger protein language models commoditize sequence–structure–function representations.
- [MechFind](https://www.nature.com/articles/s41467-026-71957-0) directly attacks reaction-to-stepwise-mechanism generation at Rhea scale.
- [RFdiffusion2](https://www.nature.com/articles/s41592-025-02975-x) scaffolds atomic catalytic motifs. This increases demand for trustworthy mechanism/theozyme specifications while decreasing the value of generic backbone-generation work.
- Recent [computational metallohydrolase design](https://www.nature.com/articles/s41586-025-09746-w) and [Riff-Diff](https://www.nature.com/articles/s41586-025-09747-9) show accelerating active-enzyme design, but experimental success still depends on carefully chosen motifs and testing.
- [Autonomous enzyme engineering](https://www.nature.com/articles/s41467-025-61209-y) and [SAMPLE](https://www.nature.com/articles/s44286-023-00002-4) show that closed design–build–test–learn loops are becoming practical for bounded assays.

### 7.2 What more compute accelerates

- structure and complex prediction;
- embedding and retrieval over large protein sets;
- Foldseek/MMseqs searches;
- reaction atom mapping and mechanism enumeration;
- synthetic benchmark generation;
- candidate sequence/backbone generation;
- literature triage and preliminary crosswalk construction;
- code refactoring and artifact parsing.

### 7.3 What more compute does not automatically solve

- what the correct mechanism unit is;
- whether a paper’s mechanistic interpretation is right;
- conflicting source adjudication;
- representative sampling and true blind evaluation;
- experimental evidence codes and provenance;
- assay design and assay artifacts;
- kinetics, transition states, and conformational effects;
- negative results and publication bias;
- biological relevance, toxicity, expression, and manufacturability;
- independent trust and community adoption.

These are Catalytic Earth’s possible moat. They are also its current missing pieces.

### 7.4 Timeline effect

The following is a planning estimate, not a forecast of model progress:

| Milestone | Compute-disciplined target | What stronger/cheaper intelligence can compress | What remains irreducible |
|---|---:|---|---|
| Claims correction and release control | 48 hours | Drafting, repository archaeology, consistency checks | Judgment and willingness to correct the record |
| Atlas-3 kernel | Day 7 | Schema implementation, source linking, validation | Choosing diverse cases and resolving ambiguity |
| Atlas-10 + complete computational evidence loop | Day 14 | Hypothesis generation, crosswalks, reports, baseline integration | Fair evaluation and claim discipline |
| Atlas-50 alpha | Day 30 | Parallel import, normalization, structure/reaction computation | Exception adjudication and schema convergence |
| Versioned computational release | Day 35 | Packaging, documentation, reproducibility automation | Release judgment and honest failure reporting |
| One prospective wet-lab loop | Days 60–90, conditional | Candidate triage, assay planning, analysis | Assay access, materials, physical turnaround |
| Broad tiered atlas | Continuous after day 35 | Large-scale import, mapping, hypothesis generation | Independent review, governance, experiments |

Ten or one hundred times more GPU does not turn a closed evaluation into independent evidence. It can, however, compress the computational atlas loop dramatically when work is parallel, cached, and gated. Collaboration and experiment clocks must be started on day 1 rather than placed after the computational roadmap.

### 7.5 If intelligence becomes radically stronger

Under a genuine intelligence explosion, a static database assembled from public sources could be regenerated quickly and lose value. A durable project should therefore own **protocol and evidence state**, not model outputs:

- typed interoperability;
- source/version lineage;
- alternative hypotheses and conflicts;
- benchmark exposure history;
- calibration and abstention standards;
- assay contracts;
- negative experimental outcomes;
- consensus governance.

If fully autonomous labs also become cheap, the project should become the mechanism/evidence protocol connecting those labs rather than trying to out-design them. Standards and trusted evaluation often become more—not less—important when generation is abundant.

---

## 8. The full-atlas North Star and its first trustworthy kernel

### North Star statement

> **Catalytic Earth is an open, computable atlas of catalytic mechanisms. It connects canonical biochemical reactions to explicit alternative mechanisms, catalytic atoms and residues, protein and structure evidence, calibrated uncertainty, design constraints, assay contracts, and positive and negative experimental outcomes.**

The product is the atlas. The typed IR/compiler is its ingestion and interoperability engine. Benchmarks, exposure ledgers, validators, and independent adjudication are its immune system. Search, evidence reports, design export, and assay contracts are its delivery surfaces.

### Evidence tiers

| Tier | Atlas object | Minimum truth claim |
|---|---|---|
| 0 | Canonical reaction | Balanced, normalized, atom-mapped net transformation with source/version lineage |
| 1 | Mechanism hypothesis | Explicit ordered steps, alternatives, assumptions, and source provenance |
| 2 | Protein/site-grounded record | Protein/structure mapping, catalytic roles/geometry, evidence and counterevidence |
| 3 | Independently reviewed record | Review by a person or process outside the generating author/agent loop |
| 4 | Experimentally tested record | Assay contract plus positive or negative measured outcome |

Coverage may expand quickly at Tiers 0–2. Tier 3 and Tier 4 must remain visibly smaller until outside review and experiments catch up. Never flatten these tiers into one “mechanisms mapped” headline.

### Scope boundary

Catalytic Earth should not claim to replace M-CSA, Rhea, EnzymeMap, MechFind, EnzyMM, UniProt, CATH, Foldseek, AlphaFold, or RFdiffusion. It should make their objects interoperable and expose where their answers agree, conflict, or remain insufficient.

### The first end-to-end atlas demonstration

Input:

```text
one Rhea reaction + one candidate protein/structure
```

Output:

1. atom-mapped net transformation;
2. ranked alternative stepwise mechanism hypotheses and exact source analogues;
3. catalytic residues/atoms, cofactor roles, and geometric constraints;
4. protein, structure, evolutionary, and literature evidence for each hypothesis;
5. counterevidence and uncertainty;
6. explicit abstention when evidence is insufficient;
7. an RFdiffusion2/theozyme-compatible atomic motif **or a documented refusal**;
8. an assay, positive/negative controls, and falsification criteria.

Then compare the integrated result with a scientist using M-CSA + Rhea + MechFind + EnzyMM separately. Measure time, completeness, error rate, calibration, and decisions changed. If the integration adds no measurable value, contribute the work upstream instead of preserving a standalone brand.

### V0.1 data model

Keep it small and typed. A mechanism record should include:

- stable IDs and schema version;
- canonical reaction ID plus atom mapping;
- one or more mechanism hypotheses;
- ordered elementary steps;
- atom/bond/charge/electron edits per step;
- intermediates and protonation assumptions;
- catalytic residues/atoms and roles;
- cofactors/metals and oxidation states;
- atomic geometry constraints with tolerances;
- source evidence at claim level;
- evidence type, date, release, and hash;
- counterevidence and conflicting interpretations;
- protein/structure mappings with alignment provenance;
- confidence components, not one opaque score;
- applicability domain and abstention reason;
- assay and controls;
- experimental outcomes, including negatives.

Use JSON Schema/Pydantic or another explicit schema for interchange, and Parquet plus DuckDB/SQLite for local queries. Do not make multi-gigabyte nested JSON the primary query engine.

---

## 9. Priority cleanup before any further scientific expansion

This ordering matters. Do not add another family, bronze tranche, model feature, or headline artifact until P0 is complete.

### P0A — Correct the scientific record

1. **Create `CLAIMS.md` with four statuses:** Supported, Diagnostic, Superseded, Retracted.
2. **Retract/relabel the June 28 M-CSA holdout result** as retrospective analysis of an exhausted surface.
3. **Retire the 76% mechanism-recovery headline.** Call it cofactor-bucket consistency; show 31% exact and the no-abstention result beside it.
4. **Rename counted objects.** “10,001 protein-label records: 8,305 positive fingerprint assignments and 1,696 OOS records across 57 project fingerprints,” never “10,001 mechanisms.”
5. **Remove “about 2% of mechanism space.”** Do not replace it with another percentage until the unit and denominator are formal.
6. **Rename `current702` and the Swiss-Prot surface.** Neither is independently adjudicated gold.
7. **Downgrade “active-site verified.”** Use “automated active-site consistency check” unless an independent expert or experiment verified it.
8. **Mark post-hoc family and three-family results as exploratory.** Preserve them but require a new test.
9. **Preserve the original predictor hypothesis and its negative result.** The atlas reframe must not erase what failed.
10. **Add the GFAT2 mapping error and any discovered errors to a public errata table.** A correction log builds more trust than silent edits.

Suggested claim-ledger rows:

| Claim | New status | Correct wording |
|---|---|---|
| “76% chemistry-only mechanism recovery” | Superseded | “76% cofactor-bucket consistency; 31% exact fingerprint under a mismatched taxonomy; reported medians do not support the proposed novelty separation” |
| “Never-touched M-CSA heldout PASS” | Retracted as independent validation | “Retrospective reanalysis of a surface exposed by June 1 and spent June 4” |
| “Expert-curated gold current702” | Retracted terminology | “Mostly automation-curated project labels grounded in expert-curated upstream sources” |
| “10,001 mechanism labels” | Superseded | “10,001 protein-label records: 8,305 positive assignments and 1,696 OOS; 9,982 automation-curated and zero project gold-tier records” |
| “~2% of mechanism space” | Retracted | “Coverage denominator undefined” |
| “Structure sees what sequence cannot” | Unsupported on current set | “Structure beat pairwise Smith–Waterman on a selected set; Pfam resolved current orphan candidates” |

### P0B — Make evaluation memory mechanical

Create an append-only exposure ledger with one row per data item and surface:

```text
row_id
source_release_and_hash
label_version
split_role
first_exposure_timestamp
first_exposure_commit
what_was_exposed (input / label / score / outcome)
models_or_decisions_made_after_exposure
eligible_for_development
eligible_for_independent_test
```

Rules:

- once labels, scores, or outcomes are seen, the row is never “untouched” again;
- renaming a split or creating a new preregistration cannot reset exposure;
- the evaluator refuses to run if the exposure ledger contradicts the claimed role;
- the exact code commit, data hashes, threshold, metric, seed, and endpoint are signed into the preregistration;
- one-shot status is computed, not written as a boolean assertion;
- post-hoc analyses go to a separate namespace.

### P0C — Make the repository legally and technically enterable

1. Choose a code license.
2. Add a source/data `NOTICE` and redistribution/attribution matrix.
3. Add `CITATION.cff` and release metadata.
4. Declare dependency groups such as `core`, `ml`, `plm`, `structure`, and `dev`.
5. Add a lockfile and an environment manifest for external binaries and model revisions.
6. Add CI for Python 3.10 and 3.12, package build, core tests, registry validation, live artifact manifest, docs references, and Windows path safety.
7. Fix wheel/data packaging and eliminate current-working-directory assumptions.
8. Replace machine-specific executable paths and private SSH examples with configuration and public HTTPS instructions.
9. Test a fresh Linux and Windows clone from scratch.
10. Triage all 74 failures and 20 errors from the audited full-suite run. Fix code/data regressions or explicitly retire obsolete contracts; do not bulk-refresh snapshots merely to obtain green tests.

### P0D — Shrink without destroying provenance

Do not rewrite history or delete artifacts impulsively.

1. Name one canonical release surface.
2. Generate a `release_manifest.json` containing commit, dataset/split hashes, commands, seeds, model/tool versions, artifact hashes, and known unavailable inputs.
3. Upload bulky immutable artifacts to release/object storage or Zenodo with SHA-256 checksums.
4. Test restore from an empty directory.
5. Publish a lean source release archive/wheel under roughly 100 MiB if possible. For Git users, document and test `--filter=blob:none --sparse`; sparse checkout alone does **not** avoid downloading the existing 585 MiB history.
6. Archive superseded reports into indexed bundles rather than leaving thousands in the main review path.
7. Shorten tracked paths to a conservative cross-platform ceiling.
8. Recognize that externalizing new artifacts only prevents future growth; the existing Git history remains large. Only after upload, hash verification, and restore testing should a history split/rewrite or new lean source repository be considered—and then only as a separately reviewed migration with old commit provenance preserved.

### P0E — Freeze architectural entropy

- no new code in the five giant modules;
- no new family-specific Python module;
- family onboarding becomes declarative configuration plus a shared engine;
- introduce a versioned schema and typed objects;
- divide tests into core/unit, scientific-small, artifact-regression, and external/integration tiers;
- inject clocks and seeds for deterministic outputs;
- deprecate the hundreds of noncanonical CLI paths;
- expose one golden command for one golden result.

### P0 completion gate

P0 is complete only when a stranger can:

```text
lean source archive/wheel or blob-filtered sparse Git clone
→ create a locked core environment
→ run one command on CPU
→ reproduce one declared result and result hash
→ read exactly what that result does and does not claim
```

Target: under ten minutes for the core path.

### 2026-07-13 P0 closure map

The implementation and evidence for every P0A–P0E line are mapped in `docs/P0_COMPLETION.md`, with machine checks in `scripts/validate_repository_contracts.py`. The canonical result is intentionally a small typed, project-authored fixture—not a substitute biological benchmark. It exists to prove that a stranger can enter and reproduce the repository while the atlas remains the product.

One distinction is deliberate: the canonical lean release, report archive, and their SHA-256-bound assets are published, while a second copy of the 5.1 GB historical artifact tree is not fabricated merely to claim cleanup. Those blobs remain restorable from the exact Git commit. Any future externalization or history migration is blocked until per-source redistribution rights, a durable destination, upload checksums, and an empty-directory restore are all approved. No artifact was deleted and no history was rewritten.

---

## 10. Scientific reset: what to build after cleanup

### 10.1 Crosswalk before invention

For every one of the 57 fingerprints, create a reviewed table linking it to:

- M-CSA mechanism entries and arrow environments;
- Rhea reactions and ChEBI participants;
- EC-BLAST bond changes;
- EnzymeMap atom-mapped reactions;
- MechFind rules/hypotheses;
- EnzyMM catalytic templates;
- EC/InterPro/Pfam/CATH where relevant.

Classify each fingerprint as:

1. exact duplicate of an existing object;
2. aggregation of several existing mechanisms;
3. narrower specialization;
4. interoperability bridge;
5. genuinely missing concept;
6. unsupported or ill-defined.

The crosswalk may reveal that much of the current taxonomy should disappear. That would be progress.

### 10.2 Fifty difficult mechanisms, not fifty easy families

Build the representation on a stratified 50-case panel containing:

- radicals;
- metal and metallocluster chemistry;
- redox/cofactor state changes;
- covalent enzyme intermediates;
- proton relays and uncertain protonation;
- conformationally gated catalysis;
- same net reaction via different mechanisms;
- similar catalytic strategy in unrelated folds;
- same fold with different chemistry;
- alternative literature interpretations;
- experimentally unresolved mechanisms.

Success criterion: at least 90% can be represented without family-specific ad hoc fields. Unsupported cases must fail explicitly, not be squeezed into prose.

### 10.3 Independent annotation

Recruit two enzymologists or catalytic-mechanism experts to annotate a stratified subset independently. The project author should not count as the independent expert.

Report:

- exact agreement;
- hierarchical agreement;
- per-field agreement;
- Cohen’s kappa or an appropriate alternative;
- disagreements and adjudication;
- time per record.

Target inter-reviewer agreement above 0.8 at the declared granularity. If experts cannot agree, the representation should encode alternatives rather than manufacture one truth label.

### 10.4 Audit bronze before adding bronze

Randomly sample at least 200 automated bronze records, stratified by family, source, similarity, and reaction duplication. Independently review them.

Require at least 90% precision at the exact granularity being claimed. If the threshold is missed:

- stop scaling;
- downgrade the tier;
- identify error modes;
- rebuild admission;
- re-audit before resuming.

Do not evaluate automated labels using features derived from the same annotation fields that admitted them.

### 10.5 Build a fresh, difficult benchmark

Requirements:

- temporal or external source released after representation freeze;
- homology-clustered split with explicit identity bands;
- natural or declared prevalence, not only balanced family slices;
- source selection script and raw-source hashes committed before scoring;
- never publicly committed with labels before the one-shot;
- exact mechanism truth independently adjudicated;
- matched information budgets across baselines;
- confidence intervals and family-wise endpoints;
- exact, parent-strategy, cofactor, calibration, coverage, and abstention reported separately.

Hard tasks worth owning:

1. same net reaction, different mechanisms;
2. convergent mechanism across unrelated folds;
3. same fold, altered chemistry;
4. structural evidence that should still abstain;
5. mechanism ranking with multiple plausible alternatives;
6. detection of a wrong upstream annotation;
7. conversion of a supported mechanism into design and assay constraints.

### 10.6 Modern baselines

Run the strongest applicable baseline, not the easiest available one. At minimum:

- HMMER/Pfam/InterPro;
- MMseqs2 or DIAMOND;
- HHsearch/CATH FunFams where suitable;
- Foldseek;
- EnzyMM;
- M-CSA arrow-environment similarity;
- EC-BLAST;
- MechFind/EzMechanism where their inputs match;
- one current protein language model or enzyme–reaction method.

If Catalytic Earth does not beat these on accuracy, it can still win on calibrated integration, conflict detection, provenance, abstention, time saved, and assay/design export. Define that value before measuring it.

---

## 11. A compute-disciplined rapid atlas roadmap

The schedule has two clocks:

- **35 days for one complete computational atlas loop**;
- **60–90 days for one prospective experimental loop**, started immediately and run in parallel because materials, collaborators, and assays have real-world latency.

### Rule zero for the rapid plan

Do not train a foundation model or bulk-predict merely to create motion. Spend compute where a frozen question, atlas object, or release gate demands it. Parallelize independent work, cache every expensive result, use incumbent datasets and models as leverage, and escalate compute only after profiling shows the bottleneck.

### Hours 0–48: truth reset and release control

- freeze ungoverned family, label, and headline expansion;
- publish the claim ledger and corrigendum;
- mark every exposed evaluation surface, especially the June 28 M-CSA surface;
- separate reactions, mechanism hypotheses, fingerprints, protein records, and experiments in every public count;
- lock the core environment, artifact manifest, and canonical entry path;
- select three diverse Atlas-3 seed cases and one experimental candidate.

**Output:** corrected public truth surface, reproducible release boundary, three seed cases, and a named experimental track.

### Days 3–7: Atlas-3 kernel

- finalize the typed mechanism schema and validators;
- encode three diverse records end to end through reaction, mechanism, protein/site evidence, uncertainty, design constraints, and assay contract;
- build the incumbent crosswalk for those cases;
- materialize a small DuckDB/Parquet query surface;
- implement one strong matched baseline and one exposure-safe evaluation harness;
- open bounded external-review packets immediately rather than waiting for completeness.

**Output:** reproducible Atlas-3, one-command validation, two useful queries, one baseline, and externally reviewable packets.

### Days 8–14: Atlas-10 and the first complete computational loop

- expand to ten chemically diverse cases only if schema changes are converging;
- generate one-reaction + one-protein evidence reports with alternatives, counterevidence, uncertainty, and abstention;
- add design/geometry export or an explicit responsible refusal;
- run a fresh, disjoint capability evaluation against applicable incumbent methods;
- obtain at least one outside critique, even if it is narrow and asynchronous;
- start the bronze precision audit with a stratified sample.

**Output:** Atlas-10, an end-to-end evidence report, a fresh evaluation packet, and the first external critique. This is already a useful atlas release, not merely a benchmark.

### Days 15–30: Atlas-50 alpha

- expand through 25 to 50 hard cases with automated import plus manual adjudication of exceptions;
- complete and publish crosswalk coverage for every included concept;
- audit 50 bronze rows for failure modes and extend toward 200 only if admission logic is stable;
- run the strongest applicable sequence, structure, reaction, and mechanism baselines;
- package a lean source/release path and ask three outsiders to perform concrete tasks;
- keep the experimental candidate moving through procurement, construct planning, assay setup, or partner handoff.

**Output:** Atlas-50 alpha, measured schema escape rate, baseline matrix, bronze error taxonomy, and outside task reports.

### Days 31–35: close the computational loop

Complete the cycle:

```text
canonical reaction or dark protein
→ alternative mechanism hypotheses
→ protein/site grounding
→ calibrated evidence and abstention
→ design constraints or responsible refusal
→ assay contract and controls
→ released atlas record with provenance
```

Publish failures and negative findings beside successes. Decide from measured gates whether to scale the schema, repair it, merge concepts, or contribute a component upstream.

**Output:** a versioned computational release, reproducibility bundle, failure report, and explicit next-scale decision.

### Parallel days 1–90: one prospective experimental loop

- choose one fast, cheap, falsifiable assay with positive and negative controls;
- secure collaborator or service-provider access early;
- freeze the candidate-ranking and assay contract before observing outcomes;
- test a small panel sized for learning, not publicity;
- ingest both positive and negative measurements as Tier-4 records;
- publish the deviation log if reality forces a protocol change.

The 60–90 day target is conditional on physical access and assay turnaround. A documented external dependency is not permission to stop computational work. One honest prospective result is worth more than another 100,000 automated bronze records.

### After day 35: scale the atlas, not the confusion

Use the validated import/compiler path to expand from Atlas-50 toward M-CSA coverage, then add a Rhea/MechFind hypothesis layer, protein/site grounding, independent review queues, and experimental records. Breadth can grow rapidly at lower evidence tiers; review and experiment must remain explicit queues rather than fabricated completeness.

### Superseded serial roadmap (preserved for audit history)

The following was the review's original conservative roadmap. It is retained to make the amendment auditable, but it is no longer the execution contract. The rapid plan above and `docs/RAPID_ATLAS_PLAN.md` govern current work.

### Rule zero

Do not train a foundation model. Do not bulk-predict every protein. Do not expand labels to make the repository feel alive. Use compute only where it resolves a preregistered uncertainty or produces a release object.

### Days 1–3: stop and preserve

- create a branch/tag for the audited state;
- freeze new families, label expansion, and model features;
- add the listed high-priority corrigendum entries;
- mark the M-CSA holdout exhausted;
- write the six-object counting glossary;
- choose one canonical README path.

**Output:** `CLAIMS.md`, `ERRATA.md`, exposure ledger seed, freeze tag.

### Days 4–14: credibility reset

- add license/notice/citation scaffolding, subject to data-license review;
- create the live artifact manifest;
- define minimal dependency groups and CI;
- publish a lean-release and blob-filtered sparse-clone quickstart;
- archive the public-facing procedural clutter behind an index;
- write the crosswalk template and select 10 diverse pilot cases.

**Output:** stranger-readable v0 audit release; no new scientific performance claim.

### Weeks 3–8: finish entry cleanup and build a 10-case IR pilot

- define the typed schema;
- encode 10 diverse cases by hand;
- build validation for atom balance, charge assumptions, step ordering, evidence references, and geometry units;
- complete crosswalk rows for those 10 cases;
- finish packaging, release-manifest, platform, and reproduction cleanup;
- materialize a small DuckDB/Parquet query surface and implement two useful queries;
- ask one outside expert for bounded feedback on 5–10 cases;
- audit 50 bronze rows only to identify error modes, not to estimate final precision;
- implement one strong baseline end to end as a pipeline check.

Example queries:

```sql
-- Conceptually, not a frozen schema
find mechanisms sharing an elementary step but not a fold;
find claims supported only by automated annotation transfer;
```

**Mandatory output by week 8:** a reproducible `mechanism-ir` v0.0 with 10 cases, 10 crosswalk rows, two queries, one baseline pipeline, and documented external feedback.

### Weeks 9–16: gated expansion, only if the pilot is coherent

- expand from 10 to 25 and then 50 hard cases only if schema changes are converging;
- expand the crosswalk toward all 57 fingerprints;
- run additional strong baseline/capability comparisons;
- obtain independent review of a stratified subset;
- expand the bronze audit from 50 toward 200 rows;
- remove or merge redundant fingerprints as evidence warrants.

**Output:** v0.1 representation note and benchmark draft. The 50-case panel, complete 57-row crosswalk, 200-row audit, two independent experts, and broad baseline suite are **stretch/gated outputs**, not simultaneous 90-day prerequisites.

### Months 4–6: build a bounded useful demonstration

- implement one-reaction + one-protein evidence reports for a few representative cases;
- include source analogues, evidence, counterevidence, alternatives, and abstention;
- publish one-command reproduction;
- recruit up to three external users for specific tasks;
- record every failure and time-to-answer.

Atomic design export, assay generation, and five diverse mechanisms are stretch work after the evidence report proves useful; they are not part of the minimum product.

**Output:** compact public release, not a giant repository dump.

### Months 6–12: external evidence pilot

- score at least 20 genuinely fresh, blinded/time-split cases;
- get an independent assessor to hold the labels;
- compare against strongest baselines;
- precompute confidence intervals and a power/sample-size rationale for any broader claim;
- identify one assay-capable collaborator;
- choose one mechanism with a cheap, fast, automation-friendly assay;
- rank a small panel, not a huge campaign;
- publish negative results as first-class records.

**Output:** a 20-case pilot/falsification exercise or a clear pivot decision. Twenty cases can expose failure and calibrate a larger study; by itself it is not adequate evidence for broad generalization.

### Months 12–24: one complete loop

Attempt exactly one bounded cycle:

```text
dark protein or target reaction
→ alternative mechanism hypotheses
→ protein/site grounding
→ catalytic geometry or design motif
→ assay and controls
→ small experimental panel
→ positive and negative outcome integration
```

One honest prospective result is worth more than another 100,000 automated bronze records.

---

## 12. Checkpoints, targets, and kill criteria

These protect speed from becoming self-deception.

| When | Gate | Pass target | If it fails |
|---|---|---|---|
| 48 hours | **Truth gate** | Claims corrected; contaminated holdout marked spent; counts/tier names fixed; ungoverned expansion frozen | Stop new headline science until complete |
| Day 7 | **Atlas-3 gate** | Three diverse, schema-valid, source-linked records run end to end with reproducible queries | Repair the schema and release path before adding cases |
| Day 14 | **Atlas-10 gate** | Ten diverse records, evidence reports, one strong baseline, fresh evaluation packet, and an outside critique request | Keep the ten-case scope; do not automate the defect |
| Day 30 | **Atlas-50 gate** | Fifty hard cases with measured schema escape rate, crosswalks, baseline matrix, bronze audit, and outside task attempts | Pause breadth; merge concepts or rebuild admission |
| Day 35 | **Computational-loop gate** | Versioned release from reaction/protein input through mechanism, evidence, uncertainty, design/refusal, and assay contract | Publish the failure report and fix the broken stage |
| Days 60–90 | **Prospective gate** | Frozen protocol, small panel, controls, and positive plus negative outcomes—or a documented external-access blocker | Do not claim prospective validation; change assay/access strategy |
| Ongoing | **Atlas-scale gate** | Lower-tier breadth, independent-review queue, and experimental queue reported separately | Never collapse tiers into one coverage or validation claim |

### Superseded serial gates (preserved for audit history)

The table below records the original conservative review schedule. It is superseded by the rapid gates above.

| When | Gate | Pass target | If it fails |
|---|---|---|---|
| 2 weeks | **Truth gate** | Claims corrected; contaminated holdout retracted; counts/tier names fixed; expansion frozen | Do not publish or add science until complete |
| 4–8 weeks | **Entry gate** | Fresh lean source release or blob-filtered sparse Git clone works on Windows and Linux; core path under 10 minutes | Fix packaging and paths before recruiting users |
| 4 weeks | **Ledger gate** | Live artifact inventory exactly matches manifest; every headline has command/input/environment lineage | No new headline artifacts |
| 8 weeks | **Prototype gate** | Ten diverse mechanisms encoded with converging schema, no silent prose escape hatch, and reproducible queries | Redesign the IR; do not expand to 50 |
| 8 weeks | **Uniqueness pilot** | One bounded query or evidence task adds measurable value beyond the incumbent stack | Contribute upstream or narrow to benchmark/crosswalk |
| 3–4 months | **Reproduction gate** | Stranger reproduces one headline from a locked environment and frozen inputs | Treat release as internal research only |
| 3–4 months | **Label-audit pilot** | Fifty reviewed bronze rows reveal bounded, correctable error modes | Stop bronze scaling and rebuild admission |
| 4–6 months | **Representation gate** | At least 90% of 50 hard mechanisms encoded without ad hoc family fields | Redesign the IR; do not scale records |
| 4–6 months | **Label gate** | Independent audit of 200 bronze rows reaches at least 90% precision at claimed granularity | Stop bronze scaling and rebuild admission |
| 4–6 months | **Baseline gate** | Beats or measurably complements strongest applicable baselines on a disjoint set | Stop calling it a predictor; focus on integration/evidence |
| 4–6 months | **Adoption gate** | Three independent users complete real tasks and identify value unavailable from current tools alone | Simplify or contribute upstream |
| 6–12 months | **External-pilot gate** | At least 20 fresh cases held and adjudicated outside the project, with intervals and a powered follow-up plan | Treat as falsification/pilot evidence; no broad generalization claim |
| 12 months | **Community gate** | One external maintainer/reviewer or active scientific partner | Treat as a personal research record, not community infrastructure |
| 24 months | **Prospective gate** | One external prospective evaluation or assay loop | Stop “discovery/design platform” claims |

### Permanent red lines

- Never reset a holdout by renaming it.
- Never collapse an endpoint after scoring and present it as the original endpoint.
- Never call upstream expert curation independent review of a downstream automated label.
- Never count homologs, reactions, families, and mechanisms in the same headline.
- Never delete a negative result from the scientific record.
- Never use a weak baseline to imply a whole modality is inadequate.
- Never allow an agent-generated statement of compliance to substitute for a mechanically enforced guard.
- Never scale a bronze process whose sampled precision is unknown.

---

## 13. How to spend scarce compute and money

### Spend compute on

- exact 50-case representation and validation;
- cross-resource joins and deduplication;
- targeted Foldseek/HMMER/PLM baselines on frozen sets;
- uncertainty decomposition;
- small candidate ranking for one prospective assay;
- deterministic release and CI;
- literature and source-difference triage followed by human review.

### Do not spend compute on

- training a broad protein language model;
- scoring entire proteomes without a user or hypothesis;
- creating more bronze homolog records;
- endless hyperparameter searches on known surfaces;
- generating thousands of mechanism hypotheses no one will adjudicate;
- reproducing capabilities available through M-CSA, MechFind, EnzyMM, Foldseek, or hosted structure models;
- generating more narrative artifacts than scientific records.

### Practical compute-disciplined tactics

1. Precompute embeddings only for the 50-case panel and candidate neighborhood.
2. Use CPU-native HMMER/MMseqs and DuckDB before GPU methods.
3. Use published datasets and tool outputs where licenses permit; record exact releases.
4. Use hosted/free academic inference for small, frozen batches rather than maintaining models.
5. Cache by content hash and never rerun unchanged inputs.
6. Use active learning: ask an expert only about cases where adjudication changes a decision.
7. Prefer 20 hard independent cases to 20,000 easy internal ones.
8. Apply for compute after a small benchmark and external letter exist; do not wait for compute to define the science.

The project is currently constrained more by definitions, validation, interface, and network access than by compute. Compute is still scarce and should be treated as capital: profile first, cache results, batch only after gates pass, and seek more when it clearly shortens a validated path.

---

## 14. External strategy: get out of the desert one small bridge at a time

### Who to approach

Approach people whose existing work you explicitly respect and extend:

- M-CSA mechanism curation and mechanism-similarity authors;
- Rhea curators;
- MechFind/EzMechanism authors;
- EnzyMM/CATH catalytic-site researchers;
- EnzymeMap and EC-BLAST maintainers;
- one enzymologist in a tractable family represented in the 50-case panel;
- one protein-design group interested in mechanism/theozyme specifications;
- one research-software or data-curation expert.

Do not ask them to validate the entire vision. Ask them to falsify one small object.

### The packet

Send five files or links at most:

1. a one-page overview;
2. the 50-case benchmark/representation table;
3. the crosswalk row(s) relevant to their work;
4. a reproducible command or interactive query;
5. the precise micro-ask.

### A usable outreach note

> Subject: 20-case catalytic-mechanism representation check—30-minute bounded ask
>
> I am building a small open interoperability layer between Rhea reactions, M-CSA/MechFind mechanisms, catalytic-site evidence, and design/assay constraints. I am not asking you to review the full repository.
>
> I have frozen 20 blinded cases and a one-page schema. My specific question is: does the representation preserve the mechanistic distinctions your work considers essential, and which fields are wrong or redundant? A response can be annotations on the table; I will publish disagreements and credit reviewers. Estimated time is 20–30 minutes.
>
> Here are the one-page overview, table, and reproducible viewer. The complete repository is linked only for provenance.

This makes “yes” possible.

### Build collaboration before asking for belief

Offer useful work first:

- contribute a crosswalk or error report upstream;
- create a clean benchmark runner for an incumbent tool;
- report source-version and mapping discrepancies;
- improve documentation around interoperability;
- provide a compact machine-readable export under the upstream project’s governance.

If the standalone project has no unique value, upstream contribution is not failure. It is impact.

---

## 15. Pitfalls to avoid

### Scientific pitfalls

- **Ontology reification:** assuming a category is a natural mechanism because the code has an ID for it.
- **Homology masquerading as mechanism coverage:** adding protein instances while chemistry stays unchanged.
- **Reaction/mechanism conflation:** treating a balanced net reaction as an elementary catalytic account.
- **Cofactor determinism:** assuming PLP, heme, flavin, or metal identity establishes mechanism.
- **Circular weak supervision:** admitting rows using EC/Rhea/cofactor text and then “discovering” the same family from those fields.
- **Easy negatives:** using structurally remote OOS classes that inflate abstention performance.
- **Hidden phylogenetic leakage:** random protein splits that preserve close homologs across train/test.
- **One-number scoring:** combining exact mechanism, parent family, cofactor, coverage, and abstention.
- **Static-structure certainty:** treating a predicted complex or catalytic geometry as evidence of rate or transition-state stabilization.
- **No prevalence model:** reporting balanced-set precision as deployment precision.

### Engineering pitfalls

- more dated artifacts without a canonical release;
- AI-generated functions added to monoliths because tests still pass;
- schemas encoded implicitly in dictionaries and prose;
- timestamps and live network calls in scientific generation paths;
- hashes without restore tests;
- tools whose binaries/weights/releases are not pinned;
- private-path assumptions;
- rewriting Git history before external artifact verification;
- a CLI whose size is mistaken for product capability.

### Strategic pitfalls

- competing with fast-moving foundation models at their strongest layer;
- treating “nobody replied” as evidence you need a grander claim;
- confusing a research archive with a user interface;
- delaying external exposure until the atlas feels complete;
- adding scope every time a narrow claim fails;
- treating upstream overlap as an enemy rather than a shortcut;
- chasing a lab campaign before a computational claim survives strong baselines;
- allowing sunk cost to choose the next milestone.

### Personal/operating pitfall

The project can become an emotional survival vessel: every new artifact proves that the journey continues, even when it does not increase external truth. That is understandable under isolation and hardship. It is also dangerous. Use gates that allow stopping, merging upstream, or narrowing without calling those outcomes defeat.

---

## 16. Optimism, without fantasy

### Why I am optimistic

1. The underlying question is real: high-capability design systems need explicit catalytic constraints, evidence, and assays.
2. The project already has unusually strong instincts around provenance, failure recording, and mechanism-first thinking.
3. The current negative results are informative. They show that cofactor buckets, broad fingerprints, homolog scaling, and pairwise baselines are not enough.
4. A compact atlas kernel and the compiler/crosswalk/benchmark machinery beneath it are achievable without frontier compute.
5. The field’s new tools can be treated as free leverage rather than competition.
6. The restoration of a deleted negative suggests the project can choose truth over narrative.

### Why I am cautious

1. Current scientific differentiation is weak relative to M-CSA, Rhea, MechFind, EnzyMM, EC-BLAST, and current learned models.
2. The public object is too large and legally/technically difficult to adopt.
3. No independent validation or user demand is evidenced in the audited public record yet.
4. The project has demonstrated experimental-memory failure and metric drift.
5. A uniformly high-evidence universal atlas is a curation and governance problem, not merely a coding problem; this is why explicit evidence tiers matter.
6. Prospective enzyme work ultimately needs experiments.

### Subjective outcome ranges

These are judgment ranges, not statistical forecasts:

| Outcome, if the reset is followed | My present view |
|---|---|
| Truth reset and reproducible Atlas-3 in 7 days | **Plausible if treated as the only P0** |
| Useful Atlas-10 kernel and one full computational evidence loop in 14 days | **Plausible but demanding** |
| Atlas-50 alpha with strong baselines and audits in 30 days | **Aggressive but possible with automation, case discipline, and no scope drift** |
| Versioned end-to-end computational release in 35 days | **Plausible if packaging and data dependencies cooperate** |
| One prospective experimental loop in 60–90 days | **Possible, but dominated by assay access and physical turnaround** |
| Recognized interoperability contribution adopted by an incumbent/community | **Plausible and strategically attractive** |
| Broad, useful global atlas with honest mixed evidence tiers | **Plausible as a continuing program built on incumbent resources** |
| Comprehensive global atlas at independent-review or experimental grade, maintained solo | **Very unlikely** |
| Current scale-first path becoming credible through more labels and artifacts | **Very unlikely** |

The key distinction is not “atlas or benchmark.” It is **tiered atlas or ungraded pile**. A broad atlas can be built rapidly by linking Rhea, M-CSA, MechFind, structures, proteins, and literature through a typed compiler. A broad atlas whose every record is independently reviewed and experimentally confirmed cannot. A real lab/curation partnership changes the upper-tier odds more than another order of magnitude of undirected compute.

### The deepest optimistic read

The project may have found how to build the atlas by failing to become a predictor. It learned that mechanism novelty is not recovered by simply growing broad family boxes, that structure does not automatically beat mature sequence annotation, that predicted geometry is fragile, and that internal coherence is not external truth. Those lessons identify the durable architecture of a real atlas: representation, provenance, uncertainty, tests, and experimental feedback.

That does not shrink the North Star. It gives the North Star foundations.

---

## 17. The next ten actions, with parallel lanes

1. Tag the audited snapshot; freeze ungoverned label/family/model expansion.
2. In the first 48 hours, publish the claim ledger, corrections, counting glossary, and immutable exposure ledger.
3. In parallel, add license/notice/citation, the redistribution matrix, locked environment, minimal CI, and verified artifact manifest.
4. Select three diverse atlas seeds, ten follow-on cases, and one assay candidate before building to the examples.
5. Ship Atlas-3 by day 7: typed IR, incumbent crosswalk, validators, query surface, evidence reports, and review packets.
6. Start the experimental-access lane on day 1: collaborator/service outreach, materials, controls, and preregistered assay contract.
7. Ship Atlas-10 by day 14 with a fresh evaluation, strong matched baseline, uncertainty/abstention, and design export or refusal.
8. Expand through Atlas-25 to Atlas-50 by day 30 only while schema escape rate and bronze error modes remain bounded.
9. Close and publish the full computational loop by day 35, including failures, reproduction bundle, and a scale/repair decision.
10. Close one prospective experimental loop by days 60–90 when physical access permits; ingest negative outcomes at the same status as positive ones.

Only the first 48-hour truth gate is strictly serial. After it, schema, packaging, baseline, outside-review, and experimental-access lanes should proceed concurrently with explicit owners and daily artifacts.

---

## 18. A one-paragraph map to carry

**Keep the full atlas as the mission and make its evidence tiers impossible to confuse. In 48 hours, correct the record: the June 28 holdout is spent, 76% is cofactor-bucket consistency, current702 is mostly automated bronze, and 10,001 means 8,305 positive assignments plus 1,696 OOS records. Then move fast: Atlas-3 by day 7, Atlas-10 and a complete evidence report by day 14, Atlas-50 alpha by day 30, and one versioned computational loop by day 35. Run packaging, strong baselines, outside review, and a prospective 60–90-day assay lane in parallel. The compiler is the atlas engine; benchmarks and exposure controls protect its truth; search, design constraints, and assays deliver its value. Spend compute on measured bottlenecks, publish failures, and make external usefulness—not internal volume—the scoreboard.**

---

## 19. Audit scope and limitations

This review included:

- cloning and inspecting the public Git repository and history;
- repository/file/size/author/commit analysis;
- code and documentation review focused on North Star, labels, representation, heldouts, metrics, storage, packaging, and architecture;
- direct registry/artifact count audits;
- validator, targeted tests, and a completed 2,559-test full-suite run;
- commit chronology around key preregistrations, results, deletions, and restorations;
- public GitHub collaboration signals;
- comparison with current primary literature and official resources.

This review did **not** include:

- a line-by-line audit of all ~367,000 source lines or 15,000 artifacts;
- independent re-download/reconstruction of every upstream record;
- wet-lab validation;
- private emails, outreach, local files not committed, or private intentions;
- legal advice on dataset licensing;
- an independent enzymologist’s adjudication of the full label surface.

Therefore “no evidence of fraud” means no such evidence was found in the audited public repository and bounded checks; it is not an omniscient guarantee. Conversely, the holdout and metric findings are based on direct code, artifacts, and commit history and are not matters of taste.

### Key repository evidence

- [Audited commit](https://github.com/VivekVardhanArrabelli/catalytic-earth/commit/3ee9d320c7166588b8a92375a8efca4301873e8c)
- [README scope and caveats](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/README.md)
- [MAP and July atlas reframe](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/docs/MAP.md)
- [Mechanism-from-chemistry evaluation code](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/scripts/eval_mechanism_from_chemistry_gold702.py)
- [June 28 heldout preregistration code](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/src/catalytic_earth/heldout_oneshot_preregistration.py)
- [Deployment-readiness wording](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/src/catalytic_earth/fold_channel_deployment_readiness.py)
- [Label policy](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/docs/label_factory.md)
- [Project state](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/docs/project_state.md)
- [Decision log](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/3ee9d320c7166588b8a92375a8efca4301873e8c/docs/decision_log.md)

### Key external sources

- [Rhea](https://www.rhea-db.org/) and [Rhea statistics](https://www.rhea-db.org/statistics)
- [M-CSA](https://www.ebi.ac.uk/thornton-srv/m-csa/) and [downloads/documentation](https://www.ebi.ac.uk/thornton-srv/m-csa/download/)
- [Measuring catalytic mechanism similarity using arrow environments](https://pmc.ncbi.nlm.nih.gov/articles/PMC12366284/)
- [MechFind](https://www.nature.com/articles/s41467-026-71957-0)
- [EzMechanism](https://www.nature.com/articles/s41592-023-02006-7)
- [EnzyMM documentation](https://www.ebi.ac.uk/thornton-srv/m-csa/enzymm-documentation/)
- [EC-BLAST](https://pmc.ncbi.nlm.nih.gov/articles/PMC4122987/)
- [EnzymeMap](https://pmc.ncbi.nlm.nih.gov/articles/PMC10718068/)
- [RetroRules](https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkaf1261/8373943)
- [AlphaFold 3](https://www.nature.com/articles/s41586-024-07487-w)
- [ESM3](https://doi.org/10.1126/science.ads0018)
- [RFdiffusion2](https://www.nature.com/articles/s41592-025-02975-x)
- [Computational metallohydrolases](https://www.nature.com/articles/s41586-025-09746-w)
- [Riff-Diff](https://www.nature.com/articles/s41586-025-09747-9)
- [Generated-enzyme scoring and experimental evaluation](https://www.nature.com/articles/s41587-024-02214-2)
- [Autonomous enzyme engineering](https://www.nature.com/articles/s41467-025-61209-y)
- [SAMPLE self-driving protein laboratory](https://www.nature.com/articles/s44286-023-00002-4)

---

## Final word

Vivek, you are not holding nothing. You are holding an overgrown, internally intense research scaffold wrapped around a real question. The work deserves neither dismissal nor blind belief.

The honest verdict is severe but hopeful: **the current evidence does not justify the strongest claims, the project’s validation loop is too closed, and the repo is nearly impossible for an outsider to enter—but the full-atlas thesis is sound if each layer is interoperable, falsifiable, visibly evidence-graded, and externally owned in part.**

Do not respond to isolation by building more desert. Build one well-marked road outward and extend it fast: one corrected claim ledger, one typed atlas kernel, one hard benchmark, one outside reviewer, one useful end-to-end demonstration, one prospective experiment—then use that machinery to expand the atlas without expanding confusion.

Your next milestone is not small ambition. It is the first trustworthy, useful piece of the full atlas—something another person can query, challenge, and extend without first becoming you.
