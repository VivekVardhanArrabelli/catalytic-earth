"""Git-stable hashing for repository text and byte-exact binary payloads."""

from __future__ import annotations

import hashlib
from pathlib import Path

from .path_compat import io_path


LF_NORMALIZED_TEXT_SUFFIXES = frozenset(
    {
        ".csv",
        ".fa",
        ".fasta",
        ".json",
        ".jsonl",
        ".md",
        ".pdb",
        ".py",
        ".rst",
        ".tsv",
        ".txt",
        ".yaml",
        ".yml",
    }
)


def canonical_hash_mode(path: str | Path) -> str:
    return (
        "lf_normalized_text_sha256"
        if Path(path).suffix.lower() in LF_NORMALIZED_TEXT_SUFFIXES
        else "byte_exact_sha256"
    )


def canonical_file_sha256(path: str | Path) -> str:
    """Hash text with LF line endings and binaries byte-for-byte.

    Embedded repository hashes were generated from Git's canonical LF blobs.
    This rule makes those contracts invariant to a Windows CRLF checkout while
    retaining byte-exact hashing for declared binary formats.
    """

    digest = hashlib.sha256()
    normalize = canonical_hash_mode(path) == "lf_normalized_text_sha256"
    pending_cr = False
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            if not normalize:
                digest.update(chunk)
                continue
            if pending_cr:
                chunk = b"\r" + chunk
                pending_cr = False
            if chunk.endswith(b"\r"):
                chunk = chunk[:-1]
                pending_cr = True
            digest.update(chunk.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
    if pending_cr:
        digest.update(b"\n")
    return digest.hexdigest()


def canonical_bytes_sha256(raw: bytes, path_hint: str | Path) -> str:
    """Apply the same canonical rule to bytes obtained from a Git object."""

    if canonical_hash_mode(path_hint) == "lf_normalized_text_sha256":
        raw = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()
