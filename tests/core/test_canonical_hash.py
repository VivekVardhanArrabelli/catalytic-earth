from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.canonical_hash import (
    canonical_bytes_sha256,
    canonical_file_sha256,
    canonical_hash_mode,
)


class CanonicalHashTests(unittest.TestCase):
    def test_text_hash_is_checkout_line_ending_invariant(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            lf = Path(tmpdir) / "lf.json"
            crlf = Path(tmpdir) / "crlf.json"
            lf.write_bytes(b'{"a": 1}\n{"b": 2}\n')
            crlf.write_bytes(b'{"a": 1}\r\n{"b": 2}\r\n')
            self.assertEqual(canonical_file_sha256(lf), canonical_file_sha256(crlf))
            self.assertEqual(canonical_hash_mode(lf), "lf_normalized_text_sha256")
            self.assertEqual(
                canonical_bytes_sha256(b'{"a": 1}\r\n{"b": 2}\r\n', "x.json"),
                canonical_file_sha256(lf),
            )

    def test_binary_hash_remains_byte_exact(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            payload = Path(tmpdir) / "payload.npz"
            payload.write_bytes(b"binary\r\nbytes")
            self.assertEqual(
                canonical_file_sha256(payload),
                hashlib.sha256(b"binary\r\nbytes").hexdigest(),
            )
            self.assertEqual(canonical_hash_mode(payload), "byte_exact_sha256")


if __name__ == "__main__":
    unittest.main()
