from __future__ import annotations

import base64
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tools"))

from materialize_github_blob import (
    MaterializationError,
    atomic_write,
    build_contents_url,
    build_receipt,
    decode_contents_payload,
    git_blob_sha1,
    sha256_hex,
    verify_materialization,
)


class GithubBlobMaterializerTests(unittest.TestCase):
    def setUp(self):
        self.data = b'{"state":"PARTIAL","claim_allowed":false}\n'
        self.blob_sha = git_blob_sha1(self.data)
        self.sha256 = sha256_hex(self.data)
        self.payload = {
            "type": "file",
            "encoding": "base64",
            "content": base64.b64encode(self.data).decode("ascii"),
            "sha": self.blob_sha,
            "size": len(self.data),
        }

    def test_decodes_and_verifies_known_blob(self):
        decoded = decode_contents_payload(self.payload)
        report = verify_materialization(
            decoded,
            expected_blob_sha1=self.blob_sha,
            expected_size=len(self.data),
            expected_sha256=self.sha256,
        )
        self.assertTrue(report["identity_verified"])
        self.assertEqual(report["decoded_size_bytes"], len(self.data))

    def test_wrapped_base64_is_supported(self):
        payload = dict(self.payload)
        encoded = payload["content"]
        payload["content"] = encoded[:10] + "\n" + encoded[10:]
        self.assertEqual(decode_contents_payload(payload), self.data)

    def test_bad_encoding_rejected(self):
        payload = dict(self.payload)
        payload["encoding"] = "utf-8"
        with self.assertRaises(MaterializationError):
            decode_contents_payload(payload)

    def test_bad_blob_sha_rejected(self):
        with self.assertRaises(MaterializationError):
            verify_materialization(
                self.data,
                expected_blob_sha1="0" * 40,
            )

    def test_bad_size_rejected(self):
        with self.assertRaises(MaterializationError):
            verify_materialization(
                self.data,
                expected_blob_sha1=self.blob_sha,
                expected_size=1,
            )

    def test_bad_sha256_rejected(self):
        with self.assertRaises(MaterializationError):
            verify_materialization(
                self.data,
                expected_blob_sha1=self.blob_sha,
                expected_sha256="0" * 64,
            )

    def test_url_is_escaped_and_pinned(self):
        url = build_contents_url(
            "https://api.github.com/",
            "owner/repo",
            "indices/a file.json",
            "feature/x",
        )
        self.assertEqual(
            url,
            "https://api.github.com/repos/owner/repo/contents/indices/a%20file.json?ref=feature%2Fx",
        )

    def test_atomic_write_uses_private_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "nested" / "blob.json"
            atomic_write(target, self.data)
            self.assertEqual(target.read_bytes(), self.data)
            self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)

    def test_receipt_never_contains_token(self):
        receipt = build_receipt(
            repository="owner/repo",
            path="indices/file.json",
            ref="abc",
            source_url="https://api.github.com/example",
            output_path=Path("/tmp/file.json"),
            verification={
                "decoded_size_bytes": len(self.data),
                "git_blob_sha1": self.blob_sha,
                "sha256": self.sha256,
                "identity_verified": True,
            },
            github_reported_sha=self.blob_sha,
            github_reported_size=len(self.data),
        )
        rendered = json.dumps(receipt)
        self.assertNotIn("Authorization", rendered)
        self.assertNotIn("Bearer", rendered)
        self.assertFalse(receipt["boundaries"]["credential_recorded"])
        self.assertFalse(receipt["boundaries"]["claim_allowed"])


if __name__ == "__main__":
    unittest.main()
