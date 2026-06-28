#!/usr/bin/env python3
"""Read-only builder for the current702 reaction/cofactor sidecar.

The frozen current702 benchmark labels carry only a curator rationale -- no machine-readable
reaction equation or cofactor identity. This builder fetches, in batches, the UniProt
catalytic-activity reaction equations and cofactor names for the 702 manifest accessions and writes
them to a read-only sidecar artifact (the registry is NEVER touched). The sidecar lets a NON-circular
test featurize the EXPERT-CURATED gold benchmark with the leakage-safe mechanism representation
(cofactor classes + Rhea bond-change), so we can ask whether chemistry-only features recover the gold
mechanism classes -- centroids trained on the disjoint expansion-bronze atlas, evaluated on the gold
labels the admission engine never grouped.

Leakage-safe: the reaction equation and cofactor identity are curated chemical evidence (the same
category the representation already reads for bronze), NOT EC / protein name / prose / fingerprint.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from catalytic_earth.adapters import USER_AGENT  # noqa: E402
from catalytic_earth.registry_io import load_json  # noqa: E402

DEFAULT_MANIFEST = "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
DEFAULT_OUT = "artifacts/v3_current702_reaction_cofactor_sidecar.json"
_UNIPROT_SEARCH = "https://rest.uniprot.org/uniprotkb/search"

_REACTION_RE = re.compile(r"Reaction=(.*?);\s*(?:Xref=|EC=|Evidence=|$)")
_COFACTOR_RE = re.compile(r"Name=(.*?);\s*(?:Xref=|Evidence=|$)")


def _parse_reactions(cell: str) -> list[str]:
    if not cell:
        return []
    return [m.group(1).strip() for m in _REACTION_RE.finditer(cell) if m.group(1).strip()]


def _parse_cofactors(cell: str) -> list[str]:
    if not cell:
        return []
    return [m.group(1).strip() for m in _COFACTOR_RE.finditer(cell) if m.group(1).strip()]


_ACCESSION_RE = re.compile(
    r"^(?:[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2})$"
)


def _fetch_chunk(chunk: list[str]) -> dict[str, dict]:
    query = " OR ".join(f"accession:{a}" for a in chunk)
    params = {
        "query": query,
        "fields": "accession,cc_catalytic_activity,cc_cofactor",
        "format": "tsv",
        "size": str(max(len(chunk), 1)),
    }
    url = f"{_UNIPROT_SEARCH}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as resp:  # noqa: S310 - public UniProt REST
        text = resp.read().decode("utf-8", "replace")
    parsed: dict[str, dict] = {}
    for line in text.splitlines()[1:]:
        cols = line.split("\t")
        if not cols or not cols[0]:
            continue
        parsed[cols[0]] = {
            "reactions": _parse_reactions(cols[1] if len(cols) > 1 else ""),
            "cofactors": _parse_cofactors(cols[2] if len(cols) > 2 else ""),
        }
    return parsed


def _fetch(accessions: list[str], batch: int = 80) -> dict[str, dict]:
    # only well-formed UniProt accessions; the manifest may carry obsolete/compound ids that
    # 400 the batch query, so they are skipped (and isolated on per-batch failure).
    valid = [a for a in accessions if _ACCESSION_RE.match(a)]
    skipped = sorted(set(accessions) - set(valid))
    if skipped:
        print(f"  skipping {len(skipped)} non-UniProt-accession ids", file=sys.stderr)
    out: dict[str, dict] = {}
    for i in range(0, len(valid), batch):
        chunk = valid[i : i + batch]
        try:
            out.update(_fetch_chunk(chunk))
        except Exception as exc:  # noqa: BLE001 - isolate a bad id, keep going
            print(f"  batch {i} failed ({type(exc).__name__}); retrying per-accession", file=sys.stderr)
            for acc in chunk:
                try:
                    out.update(_fetch_chunk([acc]))
                except Exception:  # noqa: BLE001
                    print(f"    dropped {acc}", file=sys.stderr)
        print(f"  fetched {min(i + batch, len(valid))}/{len(valid)}", file=sys.stderr)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--batch", type=int, default=80)
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    rows = manifest["rows"] if isinstance(manifest, dict) else manifest
    accessions = sorted({r["accession"] for r in rows if r.get("accession")})
    print(f"current702 accessions: {len(accessions)}", file=sys.stderr)

    fetched = _fetch(accessions, batch=args.batch)

    sidecar = {
        acc: data
        for acc, data in sorted(fetched.items())
        if data["reactions"] or data["cofactors"]
    }
    with_reaction = sum(1 for d in sidecar.values() if d["reactions"])
    with_cofactor = sum(1 for d in sidecar.values() if d["cofactors"])

    payload = {
        "artifact_id": "v3_current702_reaction_cofactor_sidecar",
        "schema_version": "catalytic_earth.reaction_cofactor_sidecar.v1",
        "leakage_safe": True,
        "leakage_basis": "curated UniProt catalytic-activity reaction equation + cofactor identity = "
        "chemical/mechanistic evidence (same category the representation reads for bronze); "
        "NOT EC/name/prose/fingerprint. Registry untouched.",
        "method": "read-only batched UniProt TSV fetch (cc_catalytic_activity, cc_cofactor) for the "
        "current702 manifest accessions; writes only this sidecar artifact",
        "source_manifest": args.manifest,
        "counts": {
            "accessions_requested": len(accessions),
            "accessions_fetched": len(fetched),
            "accessions_in_sidecar": len(sidecar),
            "accessions_with_reaction": with_reaction,
            "accessions_with_cofactor": with_cofactor,
        },
        "chemistry_by_accession": sidecar,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"wrote {args.out}: {len(sidecar)} accessions "
        f"(reaction {with_reaction}, cofactor {with_cofactor})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
