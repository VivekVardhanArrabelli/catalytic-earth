# Start here

Catalytic Earth is an offline, reviewed record of enzyme catalytic mechanisms.
This page gets you from a fresh machine to a real answer, and is explicit about
which parts need nothing but Python, which replay saved results, and which need
an authorized external suite.

Three tiers, kept apart on purpose:

| Tier | Needs | Model inference? |
|---|---|---|
| **1. Local computation** | Python 3.10+ | No. Deterministic, byte-reproducible. |
| **2. Saved results replayed** | Tier 1 plus a previously saved artifact | No. |
| **3. Live external suite** | An available, authorized Rosalind component | Host-dependent. Not required for tiers 1–2. |

## Tier 1 — a real answer in under ten minutes

```sh
git clone https://github.com/VivekVardhanArrabelli/catalytic-earth
cd catalytic-earth
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate
python -m pip install -r requirements/build.lock   # locked build tools
python -m build --wheel --no-isolation --outdir dist
python -m pip install dist/catalytic_earth-0.1.0-py3-none-any.whl
```

> Install `requirements/build.lock` first. The project declares its license with
> PEP 639 metadata, which older setuptools rejects — a system setuptools 68
> fails `--no-isolation` with `project.license must be valid exactly by one
> definition`. The lock pins setuptools 80.9.0. (Alternatively drop
> `--no-isolation` and let the build fetch its own.)

Then, **from any directory**:

```sh
catalytic-earth reproduce                      # canonical result and its hash
catalytic-earth claims                         # what that result does NOT claim
catalytic-earth --help                         # every query surface
```

### The two worked examples

```sh
# A. Does H297N racemization nondetection mean all catalysis is lost?
catalytic-earth atlas-mechanism-evidence --variant H297N --endpoint isotope_exchange
```

Answer and full provenance: [`docs/briefs/H297N-endpoint-selectivity.md`](docs/briefs/H297N-endpoint-selectivity.md)

```sh
# B. Did H473N improve target product accumulation?  (source checkout required)
python scripts/query_atlas_perturbations.py --comparison tk_2020:H473N:DHB_accumulation
```

Answer and full provenance: [`docs/briefs/H473N-target-vs-competing-product.md`](docs/briefs/H473N-target-vs-competing-product.md)

**Route A runs from the installed wheel anywhere. Route B does not** — it
derives its root from its own file location and shells out to `git`, so run it
from the checkout you cloned above (`cd` back to it if you moved away).

Pass `--output <new file>` to either to save JSON. They differ in what happens
next, so create the directory first and name a fresh file every time:

- **Route A refuses an existing path** and writes nothing — the guarantee in its
  `--help` is real.
- **Route B replaces an existing file without warning.** Its script is bound by
  sha256 in `data/atlas/perturbations/review.json`, so correcting that would
  need a renewed source review rather than a quiet edit. `tests/core/
  test_perturbation_query_output.py` pins the behaviour described here.

Neither route creates a missing directory.

## Tier 2 — the interface, and replaying a saved result

```sh
python -m catalytic_earth.workbench --port 8765   # then open http://127.0.0.1:8765/
```

Loopback only, standard library only, no network calls. The ledger starts empty
and is shown as empty.

To attach an output a real external tool saved, and open it again afterwards:

```sh
python -m catalytic_earth.workbench.external_results --resolve-only \
  --case atlas10.mandelate-racemase-pputida.enolate \
  --provider-suite x --provider-tool x --action structure_view --query x --artifact x
```

See [`docs/MECHANISM_WORKBENCH.md`](docs/MECHANISM_WORKBENCH.md) for the full
import, what an association status means, and what it deliberately does not.

## Tier 3 — live external suite

Needed only for a native source or structure operation. If no authorized
component is available, tiers 1 and 2 still give a complete, honest answer with
native inspection marked pending. Nothing here fabricates a suite result.

## The ninety-second version

[**Nondetection Is Not Zero**](https://claude.ai/artifact/R1aTNPKxp5fdJoBF1dr5Wy) —
a single page covering both cases above and, more to the point, what each one
refuses to claim. Source: [`docs/nondetection-is-not-zero.html`](docs/nondetection-is-not-zero.html),
openable directly in a browser.

It is a **static explanatory companion, not the Mechanism Workbench** and not a
substitute for demonstrating the interactive tool. Every figure on it came from
the two commands above; it summarises existing curated observations returned by
those recorded queries and reports no new biological experiment.

## Using the agent skill

[`.agents/skills/catalytic-earth/SKILL.md`](.agents/skills/catalytic-earth/SKILL.md)
drives the workflow above: resolve the question to a real surface, state the
identifiers, run the read-only command, save the output with its commit, and
write a seven-heading brief. It is a **project** skill — not a Rosalind plugin,
and running it is not evidence of native tool use.

Session outputs belong in `sessions/<UTC-timestamp>/`, which is git-ignored so a
run never disturbs the repository's path contracts.

## What was actually verified here

On commit `57d688af`, Linux, CPython 3.11:

- Wheel built, installed into a clean venv, and `atlas-mechanism-evidence
  --variant H297N --endpoint isotope_exchange` run **from an empty directory
  outside the repository**. Its output is byte-identical to the source-tree run
  — both sha256 `4f65dea0783252a80fc33556cd49f84a7fd093c4f0a42d40aee92be724ba2210`.
- `scripts/query_atlas_perturbations.py --comparison tk_2020:H473N:DHB_accumulation`
  run from the source checkout; output sha256 `620755f5…`.
- Route B confirmed to fail from the wheel, exactly as documented above.
- `--no-isolation` confirmed to fail on system setuptools 68.1.2 and to succeed
  with the pinned build lock.

Still a desktop-session check, not done here: whether a ChatGPT/Codex host
discovers and invokes `.agents/skills/catalytic-earth/`, and any live external
suite operation.

This is a usability check. It is not a benchmark, and no independent scientist
has evaluated the tool.
