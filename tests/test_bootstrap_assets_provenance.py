#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_bootstrap_assets_provenance import validate

DATA = Path("data/control-plane/bootstrap-assets-provenance.v1.json")


class BootstrapAssetsProvenanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(DATA.read_text(encoding="utf-8"))

    def reject(self, mutate) -> None:
        candidate = copy.deepcopy(self.base)
        mutate(candidate)
        with self.assertRaises(ValueError): validate(candidate)

    def test_canonical(self) -> None: validate(copy.deepcopy(self.base))
    def test_loader_not_complete_bootstrap(self) -> None: self.reject(lambda d: d["authority_separation"].__setitem__("loader_apk_is_complete_bootstrap", True))
    def test_build_not_device_runtime(self) -> None: self.reject(lambda d: d["authority_separation"].__setitem__("apk_build_is_device_runtime", True))
    def test_digest_not_provenance(self) -> None: self.reject(lambda d: d["authority_separation"].__setitem__("digest_is_provenance", True))
    def test_drive_not_original_source(self) -> None: self.reject(lambda d: d["authority_separation"].__setitem__("drive_copy_is_original_source", True))
    def test_missing_count_cannot_hide(self) -> None: self.reject(lambda d: d["observed_reality"].__setitem__("architecture_tar_count_present", 4))
    def test_beta_cannot_promote(self) -> None: self.reject(lambda d: d["claims"].__setitem__("beta_installable", True))
    def test_runtime_cannot_promote(self) -> None: self.reject(lambda d: d["claims"].__setitem__("android_runtime_verified", True))
    def test_release_cannot_promote(self) -> None: self.reject(lambda d: d.__setitem__("release_allowed", True))
    def test_private_source_not_public_default(self) -> None: self.reject(lambda d: d["privacy_and_storage"].__setitem__("private_source_may_be_published_by_default", True))
    def test_producer_remains_stacked(self) -> None: self.reject(lambda d: d["producer"].__setitem__("base_pull_request", 0))


if __name__ == "__main__": unittest.main()
