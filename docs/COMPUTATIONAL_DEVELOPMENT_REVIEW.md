# Computational development review — 2026-09-05

Development no longer waits for human submissions. The owner authorized a
computational substitute for that workflow dependency. The
[policy](../data/governance/computational_review_policy.json) and
[generated gate](../data/atlas/atlas50/development_gate/status.json) permit
specific source-scoped draft operations after source checking, challenge, and
explicit adjudication. CE-012 continues to govern protected registries.

## Completed review and decisions

Three agent roles produced the corrected crosswalk, generic state probe, and
source challenge. The coordinating agent adjudicated the six disputed cases.
The [internal board](https://github.com/VivekVardhanArrabelli/catalytic-earth/blob/main/work/coordination_20260905.md) records assignments and
corrections. All roles used the same model family; the challenge was informed
by earlier work and was not blind. Errors may be correlated. This process has
not been calibrated against an independent expert reference set, so it makes
no human-equivalence, review-accuracy, or measured speedup claim.

- [Crosswalk v2](ATLAS50_CROSSWALK_V2.md) contains 57 rows, an explicit old/new
  change map, 23 provisional computational classifications and 34 unresolved
  rows. Named targets and unresolved reasons replace implicit equivalence.
  These counts are successor dispositions, not improvement or accuracy scores.
- [The state probe](ATLAS50_STATE_PROBE.md) supplies shared component/state,
  tethered-carrier, and polymer/topology fields for all six disputed cases.
  The probe is a typed sidecar; the four permitted cases now also have
  [compiled source-draft records](ATLAS_SOURCE_DRAFTS.md).
- [Source challenge](ATLAS50_SOURCE_CHALLENGE.md) checked claims against
  official mechanism/structure records, primary papers at declared inspection
  depth, and actual repository admission rules. It changed decisions rather
  than merely counting agreement.
- [Adjudications](../data/atlas/atlas50/development_gate/adjudications.json)
  preserve each source abstention, relevant challenge IDs, precise permitted
  scope, and the operations each open objection blocks.

| Case | Work permitted now | Boundary retained |
| --- | --- | --- |
| M0064 topoisomerase III | Source identity and qualitative-event annotation | No topology-dependent mechanism draft or exact DNA instance |
| M0106 pyruvate dehydrogenase E1 | Source annotation and carrier-transition draft | Carrier accession, numbered lysine and observed pose unknown; 1W85 E2 binding domain is not the lipoyl domain |
| M0107 aerobic CODH | Source annotation and fixed-assembly mechanism draft | Preserve both source alternatives and proposal-scoped cofactor states |
| M0212 nitrogenase | Source annotation and ATP-coupled association-cycle draft | No complete FeMo/P-cluster pathway or exact reactive atoms |
| M0753 HisF | Source annotation and free-ammonium cyclase half-reaction draft | No inferred HisH–HisF channel or full coupled mechanism |
| M0970 glycosyltransferase | Source annotation, including local alternatives | Unresolved polymer product and chain state block mechanism draft and exact instance |

All six permit annotation, four permit a source-scoped mechanism draft, and
none permits an exact reaction instance. A probe `PASS` describes only its
named operation. It does not admit an entire panel case at every evidence tier.
The new v4 source-draft schema carries the positive typed state fields. It
preserves the Atlas-3/10 v2/v3 objects and does not promote drafts into their
canonical reaction or protein/site-grounded tiers.

The challenge also corrected our first computational review: M0112 can be an
exact relation to DHFR at the implemented EC 1.5.1.3 **reaction-core** scope.
The previous broader aggregation rationale overstated the implemented scope.
Protein context and structure applicability remain narrower, and water supplies
the N5 proton while Asp26/Asp27 organizes the network. M0049 remains invalid
PLP evidence but valid as a separately scoped pyruvoyl candidate. The original
review JSON remains pinned as the input history; v2 controls current use.

Root's direct check also found a source-internal conflict in
[M0753](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/753/): its overall residue
role table reverses the Asp11/Asp130 roles assigned in the summary and Step 5.
The state probe assigns no resolved residue roles. The HisF adjudication adds
an explicit abstention, retained in the compiled HisF record, alongside the
conflicting source assertions.

## Operational checks

Run from the repository:

```bash
python scripts/build_atlas50_crosswalk_v2.py --check
python scripts/build_atlas50_state_probe.py --check
python scripts/build_atlas50_development_gate.py --check
python scripts/run_test_tier.py "core/unit"
python scripts/validate_repository_contracts.py
```

The gate rechecks input hashes when `require_operation(repo_root, operation,
mcsa_id)` is called. It rejects stale review inputs, dropped abstentions,
unrelated or missing source challenges, unsupported scope expansion, and any
operation blocked by an unresolved objection. A hundred agent votes cannot
override an objection. Input pins are an explicit review checkpoint; the status
builder does not silently refresh them. These are integrity and permission
checks, not an automatic proof that every scientific assessment is correct.

Draft source checks have a public-primary-source budget of 100 requests and
30 MiB per batch, with no paid services or GPU jobs. This new authority applies
to the named development objects. The July ten-lane acquisition plan and its
97 human-review packets remain intact and incomplete. Independent annotation,
gold admission, benchmark claims, protected-registry expansion, and experiments
are separate evidence decisions.

Evidence controls the review because multi-agent debate has both
[reported gains on selected reasoning tasks](https://arxiv.org/abs/2305.14325)
and [documented failure modes that can degrade correct answers](https://arxiv.org/abs/2509.05396).
Neither paper validates this enzyme-review process. Distinct roles are useful
for finding objections; they do not create statistical independence.

## Next development batch

The four permitted source-scoped drafts now compile and query through a reusable
offline path. Prioritize subsequent source batches or compiler changes by the
atlas bottleneck they remove; a demonstration or another review layer is not
an automatic prerequisite.
For M0064 and M0970, acquire evidence for the missing state variables before
requesting those blocked operations. Resolve the 34 crosswalk rows through
named source targets and explicit granularity; absence from the old bounded
source index is not evidence of database absence. Stop a branch when another
check cannot change its disposition; retain an abstention instead of cycling
agents until they agree.

Rosalind Workbench 0.2.5-research-preview is installed and enabled locally.
The installed integration exposes app launchers, not a callable research-model
endpoint in this session. No GPT-Rosalind inference or Rosalind benchmark was
run, and Research-mode entitlement is unverified. Official
[Workbench guidance](https://developers.openai.com/blog/rosalind-workbench)
describes separate Research access. The review above was completed with the
available agents and source tools; it does not depend on that access.
