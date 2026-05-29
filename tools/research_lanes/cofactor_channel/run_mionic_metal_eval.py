from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
import torch.nn.functional as F


METAL_OUTPUT_INDICES = {
    "CA": 0,
    "CO": 1,
    "CU": 2,
    "FE2": 3,
    "FE": 4,
    "MG": 5,
    "MN": 6,
    "ZN": 9,
}


class SelfAttention(nn.Module):
    """M-Ionic-compatible self-attention with the intended head dimension."""

    def __init__(self, num_hidden: int, num_heads: int = 4) -> None:
        super().__init__()
        self.num_heads = num_heads
        self.attention_head_size = int(num_hidden / num_heads)
        self.all_head_size = self.num_heads * self.attention_head_size

    def _transpose_for_scores(self, x: torch.Tensor) -> torch.Tensor:
        shape = x.size()[:-1] + (self.num_heads, self.attention_head_size)
        return x.view(*shape).permute(0, 2, 1, 3)

    def forward(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        mask: torch.Tensor | None = None,
    ) -> torch.Tensor:
        q = self._transpose_for_scores(q)
        k = self._transpose_for_scores(k)
        v = self._transpose_for_scores(v)
        scores = torch.matmul(q, k.transpose(-1, -2))
        if mask is not None:
            scores = scores + (1.0 - mask) * -10000
        scores = nn.Softmax(dim=-1)(scores)
        outputs = torch.matmul(scores, v)
        outputs = outputs.permute(0, 2, 1, 3).contiguous()
        return outputs.view(*outputs.size()[:-2], self.all_head_size)


class PositionWiseFeedForward(nn.Module):
    def __init__(self, num_hidden: int, num_ff: int) -> None:
        super().__init__()
        self.W_in = nn.Linear(num_hidden, num_ff, bias=True)
        self.W_out = nn.Linear(num_ff, num_hidden, bias=True)

    def forward(self, h_v: torch.Tensor) -> torch.Tensor:
        return self.W_out(F.leaky_relu(self.W_in(h_v)))


class TransformerLayer(nn.Module):
    def __init__(
        self,
        num_hidden: int = 128,
        num_heads: int = 4,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.ModuleList(
            [nn.LayerNorm(num_hidden, eps=1e-6) for _ in range(2)]
        )
        self.attention = SelfAttention(num_hidden, num_heads)
        self.dense = PositionWiseFeedForward(num_hidden, num_hidden * 4)

    def forward(self, h_v: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        dh = self.attention(h_v, h_v, h_v, mask)
        h_v = self.norm[0](h_v + self.dropout(dh))
        dh = self.dense(h_v)
        h_v = self.norm[1](h_v + self.dropout(dh))
        if mask is not None:
            h_v = h_v * mask.squeeze(1).squeeze(1).unsqueeze(-1)
        return h_v


class IonicProtein(nn.Module):
    """M-Ionic residue classifier architecture for the released checkpoint."""

    def __init__(
        self,
        feature_dim: int,
        hidden_dim: int = 128,
        num_encoder_layers: int = 4,
        num_heads: int = 4,
        augment_eps: float = 0.05,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        self.augment_eps = augment_eps
        self.input_block = nn.Sequential(
            nn.LayerNorm(feature_dim, eps=1e-6),
            nn.Linear(feature_dim, hidden_dim),
            nn.LeakyReLU(),
        )
        self.hidden_block = nn.Sequential(
            nn.LayerNorm(hidden_dim, eps=1e-6),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(),
            nn.LayerNorm(hidden_dim, eps=1e-6),
        )
        self.encoder_layers = nn.ModuleList(
            [
                TransformerLayer(hidden_dim, num_heads, dropout)
                for _ in range(num_encoder_layers)
            ]
        )
        for ion in ("CA", "CO", "CU", "FE2", "FE", "MG", "MN", "PO4", "SO4", "ZN"):
            setattr(self, f"FC_{ion}_1", nn.Linear(hidden_dim, hidden_dim, bias=True))
            setattr(self, f"FC_{ion}_2", nn.Linear(hidden_dim, 1, bias=True))
        self.FC_null1 = nn.Linear(hidden_dim, hidden_dim, bias=True)
        self.FC_null2 = nn.Linear(hidden_dim, 1, bias=True)

    def forward(self, protein_feat: torch.Tensor, mask: torch.Tensor) -> tuple[torch.Tensor, ...]:
        if self.training and self.augment_eps > 0:
            protein_feat = protein_feat + self.augment_eps * torch.randn_like(protein_feat)
        h_v = self.input_block(protein_feat)
        h_v = self.hidden_block(h_v)
        attention_mask = mask[:, None, None, :]
        for layer in self.encoder_layers:
            h_v = layer(h_v, attention_mask)
        outputs = []
        for ion in ("CA", "CO", "CU", "FE2", "FE", "MG", "MN", "PO4", "SO4", "ZN"):
            outputs.append(
                getattr(self, f"FC_{ion}_2")(
                    F.leaky_relu(getattr(self, f"FC_{ion}_1")(h_v))
                ).squeeze(-1)
            )
        outputs.append(self.FC_null2(F.leaky_relu(self.FC_null1(h_v))).squeeze(-1))
        return tuple(outputs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label-manifest", default="artifacts/v3_sequence_nn_label_manifest_current702_20260525.json")
    parser.add_argument("--geometry-features", default="artifacts/v3_geometry_features_1025.json")
    parser.add_argument("--sequence-manifest", default="artifacts/v3_sequence_manifest_current702_repaired_20260525.json")
    parser.add_argument("--fasta", default="artifacts/v3_sequence_distance_holdout_eval_current702_repaired_20260525.fasta")
    parser.add_argument("--checkpoint", default="../m-ionic-lite/checkpoints/esm2_t33_650M_UR50D_setB_fold1.pt")
    parser.add_argument("--out", default="artifacts/v3_borrowed_mionic_metal_eval_current702_20260529.json")
    parser.add_argument("--progress-jsonl", default="artifacts/v3_borrowed_mionic_metal_eval_current702_20260529.progress.jsonl")
    parser.add_argument("--max-sequence-length", type=int, default=1022)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    started = time.perf_counter()
    import esm
    from sklearn.metrics import average_precision_score, roc_auc_score

    label_manifest = _load_json(Path(args.label_manifest))
    geometry = _load_json(Path(args.geometry_features))
    sequence_manifest = _load_json(Path(args.sequence_manifest))
    fasta_by_alias = _parse_fasta(Path(args.fasta).read_text(encoding="utf-8"))
    rows = _heldout_clean_rows(
        label_manifest=label_manifest,
        geometry=geometry,
        sequence_manifest=sequence_manifest,
        fasta_by_alias=fasta_by_alias,
    )
    if args.limit > 0:
        rows = rows[: args.limit]

    out_path = Path(args.out)
    progress_path = Path(args.progress_jsonl)
    completed = _read_progress(progress_path)

    esm_model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    esm_model.eval()
    batch_converter = alphabet.get_batch_converter()
    ionic = IonicProtein(feature_dim=1280)
    ionic.load_state_dict(torch.load(args.checkpoint, map_location="cpu"))
    ionic.eval()

    progress_path.parent.mkdir(parents=True, exist_ok=True)
    with progress_path.open("a", encoding="utf-8") as progress:
        for index, row in enumerate(rows, 1):
            if row["entry_id"] in completed:
                continue
            scored = _score_row(
                row=row,
                esm_model=esm_model,
                batch_converter=batch_converter,
                ionic=ionic,
                max_sequence_length=args.max_sequence_length,
            )
            progress.write(json.dumps(scored, sort_keys=True) + "\n")
            progress.flush()
            print(
                f"{index}/{len(rows)} {row['entry_id']} score={scored['mionic_metal_score']:.6f}",
                flush=True,
            )

    records = list(_read_progress(progress_path).values())
    y_true = [int(row["metal_present_label"]) for row in records]
    y_score = [float(row["mionic_metal_score"]) for row in records]
    metrics: dict[str, Any] = {
        "status": "complete" if len(records) == len(rows) else "partial",
        "scored_row_count": len(records),
        "expected_row_count": len(rows),
        "heldout_metal_positive_count": sum(y_true),
        "heldout_metal_negative_count": len(y_true) - sum(y_true),
    }
    if len(set(y_true)) == 2:
        metrics["roc_auc"] = round(float(roc_auc_score(y_true, y_score)), 6)
        metrics["average_precision"] = round(float(average_precision_score(y_true, y_score)), 6)
    payload = {
        "artifact_id": "v3_borrowed_mionic_metal_eval_current702_20260529",
        "schema_version": "borrowed_mionic_metal_eval.v1",
        "created_utc": _utc_now_iso(),
        "status": metrics["status"],
        "borrowed_predictor": {
            "name": "M-Ionic",
            "repository": "https://github.com/TeamSundar/m-ionic",
            "checkpoint": "esm2_t33_650M_UR50D_setB_fold1.pt",
            "protein_score_policy": "max sigmoid residue probability across CA/CO/CU/FE2/FE/MG/MN/ZN outputs",
            "published_module_compatibility_note": (
                "The released Self_Attention permutation omits the attention-head "
                "dimension on current PyTorch; this evaluator uses the intended "
                "batch/head/residue/hidden ordering while loading the released weights."
            ),
        },
        "guardrails": {
            "no_training_performed": True,
            "heldout_labels_used_for_fit_or_threshold": False,
            "label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "ontology_registry_edited": False,
            "production_scoring_changed": False,
        },
        "scope": {
            "split_assignment": "heldout",
            "clean_experimental_ligand_context_rows": len(rows),
            "experimental_label_source": "v3_geometry_features_1025 ligand_context.cofactor_families",
            "sequence_input_only": True,
            "max_sequence_length": args.max_sequence_length,
            "label_counts": dict(Counter(row["metal_present_label"] for row in rows)),
        },
        "metrics": metrics,
        "rows": sorted(records, key=lambda item: _entry_sort_key(item["entry_id"])),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {out_path} ({metrics})")
    return 0


def _score_row(
    *,
    row: dict[str, Any],
    esm_model: Any,
    batch_converter: Any,
    ionic: IonicProtein,
    max_sequence_length: int,
) -> dict[str, Any]:
    sequence = str(row["sequence"])
    truncated = sequence[:max_sequence_length]
    row_started = time.perf_counter()
    _, _, tokens = batch_converter([(row["entry_id"], truncated)])
    with torch.no_grad():
        representations = esm_model(tokens, repr_layers=[33], return_contacts=False)[
            "representations"
        ][33]
        residue_embeddings = representations[0, 1 : len(truncated) + 1, :]
        mask = torch.ones(1, residue_embeddings.shape[0])
        logits = ionic(residue_embeddings.unsqueeze(0), mask)
        ion_scores = {
            ion: float(torch.sigmoid(logits[index][0]).max().item())
            for ion, index in METAL_OUTPUT_INDICES.items()
        }
    score = max(ion_scores.values()) if ion_scores else 0.0
    return {
        "entry_id": row["entry_id"],
        "sequence_id": row.get("sequence_id"),
        "sequence_length": len(sequence),
        "sequence_truncated": len(sequence) > len(truncated),
        "sequence_sha256": hashlib.sha256(sequence.encode("utf-8")).hexdigest(),
        "metal_present_label": int(row["metal_present_label"]),
        "local_cofactor_families": row["local_cofactor_families"],
        "mionic_metal_score": score,
        "ion_scores": ion_scores,
        "elapsed_seconds": round(time.perf_counter() - row_started, 3),
    }


def _heldout_clean_rows(
    *,
    label_manifest: dict[str, Any],
    geometry: dict[str, Any],
    sequence_manifest: dict[str, Any],
    fasta_by_alias: dict[str, str],
) -> list[dict[str, Any]]:
    geometry_by_entry = {
        str(row.get("entry_id")): row
        for row in geometry.get("entries", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    sequence_by_entry = {
        str(row.get("entry_id")): row
        for row in sequence_manifest.get("rows", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    rows: list[dict[str, Any]] = []
    for manifest_row in label_manifest.get("rows", []):
        if not isinstance(manifest_row, dict):
            continue
        if manifest_row.get("split_assignment") != "heldout":
            continue
        entry_id = str(manifest_row.get("entry_id") or "")
        geometry_row = geometry_by_entry.get(entry_id, {})
        if geometry_row.get("status") != "ok":
            continue
        sequence_row = sequence_by_entry.get(entry_id, {})
        sequence_record = _first_sequence_record(sequence_row)
        sequence = _lookup_sequence(entry_id, sequence_record, fasta_by_alias)
        if not sequence:
            continue
        families = _string_list(
            (geometry_row.get("ligand_context") or {}).get("cofactor_families")
        )
        rows.append(
            {
                "entry_id": entry_id,
                "sequence_id": (
                    sequence_record.get("accession_or_structure_id")
                    or sequence_record.get("accession")
                    or manifest_row.get("sequence_id")
                ),
                "sequence": sequence,
                "local_cofactor_families": families,
                "metal_present_label": int("metal_ion" in families),
            }
        )
    return sorted(rows, key=lambda item: _entry_sort_key(item["entry_id"]))


def _parse_fasta(text: str) -> dict[str, str]:
    records: dict[str, str] = {}
    header = ""
    chunks: list[str] = []

    def store() -> None:
        if not header:
            return
        sequence = "".join(chunks).strip().upper()
        first = header.split()[0]
        aliases = [first]
        parts = [part for part in first.split("|") if part]
        aliases.extend(parts)
        for part in parts:
            if part.startswith("fallback_for_uniprot:") or part.startswith("uniprot:"):
                aliases.append(part.split(":", 1)[1])
        if len(parts) >= 2 and parts[0] in {"sp", "tr"}:
            aliases.append(parts[1])
        for alias in aliases:
            records.setdefault(alias, sequence)

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(">"):
            store()
            header = line[1:].strip()
            chunks = []
        else:
            chunks.append(line)
    store()
    return records


def _lookup_sequence(
    entry_id: str,
    sequence_record: dict[str, Any],
    fasta_by_alias: dict[str, str],
) -> str:
    aliases = [
        entry_id,
        str(sequence_record.get("accession_or_structure_id") or ""),
        str(sequence_record.get("accession") or ""),
        str(sequence_record.get("sequence_id") or ""),
    ]
    for alias in aliases:
        if alias and alias in fasta_by_alias:
            return fasta_by_alias[alias]
    return ""


def _first_sequence_record(row: dict[str, Any]) -> dict[str, Any]:
    records = row.get("sequence_records", [])
    if isinstance(records, list) and records and isinstance(records[0], dict):
        return records[0]
    return {}


def _read_progress(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            rows[str(row["entry_id"])] = row
    return rows


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None]


def _entry_sort_key(entry_id: str) -> tuple[str, int, str]:
    prefix, _, suffix = str(entry_id).partition(":")
    digits = "".join(ch for ch in suffix if ch.isdigit())
    return (prefix, int(digits) if digits else -1, suffix)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
