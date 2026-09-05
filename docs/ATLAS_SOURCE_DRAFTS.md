# Reusable source-mechanism compilation

The source-draft path turns reviewed M-CSA chemistry into offline, queryable
atlas records. It addresses the gap between source review and usable chemical
content. The compiler accepts a bounded source selection and declared scopes;
its chemistry fields do not depend on enzyme-specific schema branches.

## What is represented

New mechanism-record v4 drafts carry source reaction context, competing
mechanism proposals, ordered source steps, available curved-arrow endpoints,
source residue assertions, and typed component/state context. They preserve
the source's inferred steps, unresolved fields and review abstentions. They
remain Tier 1 source-derived drafts. M-CSA participant context is not relabeled
as a balanced Rhea reaction or an exact reaction instance.

The initial batch covers M0106 pyruvate dehydrogenase E1, M0107 aerobic CODH,
M0212 nitrogenase, and M0753 HisF. Each has one record; alternative proposals
remain inside that record: five proposals contain 43 reaction steps, five
terminal states, and 148 preserved source arrow annotations. Source annotations are not duplicated into extra
records to increase the count. The existing Atlas-3/10 v2/v3 records and query
results remain unchanged. M0064 and M0970 remain subject to their existing
mechanism-draft objections.

In particular, the carrier owner/attachment gaps, unknown complete nitrogenase
cluster pathway, and conflicting HisF Asp11/Asp130 roles remain visible in the
query. Source transcription does not settle those questions or infer geometry,
atom mappings, balanced bond edits, or experimental validation.

Step `is_inferred` is true only when the source explicitly tags it as inferred;
otherwise it is null (unspecified). Missing tags do not establish that a step
was observed, and source hedging is retained in the step text.

## Use the atlas

The installed wheel includes the compiled drafts and attribution. Query it
without the repository, raw downloads, a model, or a network connection:

```bash
catalytic-earth atlas-drafts --mcsa-id M0107 --steps
catalytic-earth atlas-drafts --assembly cycle_coupled_association
catalytic-earth atlas-drafts --text lipoyl
```

Compact results omit step bodies while retaining scope, residue evidence and
abstentions. `--steps` includes the ordered source steps and available electron
flows. An empty result means no matching record in this bounded batch; it is
not a claim that no such mechanism exists elsewhere. Every response identifies
the selected source IDs and requested operation, including empty results.

## Rebuild and extend

```bash
python scripts/build_atlas_draft_sources.py --check
python scripts/build_atlas_drafts.py --check
python scripts/run_test_tier.py "core/unit"
python scripts/validate_repository_contracts.py
```

Source acquisition requires an explicit `--fetch`; checks and compilation are
offline. The downloader verifies authorizations, enforces request and byte
budgets before and during transfer, and retains source receipts, hashes,
unavailable-scheme status and attribution. The manifest specifies the selected
IDs; subsequent permitted batches use the same importer and compiler.

The source API is the maintained M-CSA interface; its old flat files are no
longer updated. Upstream also warns that homologous residue matches do not
establish conserved catalytic function. [M-CSA API documentation](https://www.ebi.ac.uk/thornton-srv/m-csa/download/)

Source redistribution follows [the recorded attribution](../data/atlas/source_drafts/SOURCE_ATTRIBUTION.md)
and CC BY 4.0 terms. Only compiled projections and attribution enter the wheel.
The source snapshots remain in the repository source package.

## Priority rule

Choose the next batch or compiler improvement by the bottleneck it removes
from building the full computable atlas. A demonstration, benchmark, new
review layer or larger row count is not an automatic prerequisite. Add one
when its result will change what we build, admit, or spend effort on. The
current continuation is further source compilation using this reusable path,
with unresolved source applicability handled at its actual affected scope.
