#!/usr/bin/env python3
"""
Unit tests for repository inventory validation.
"""

import unittest
import json
import sys
from pathlib import Path

# Ensure scripts directory is in path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

class TestRepositoryInventory(unittest.TestCase):
    """Test suite for REPOSITORY_INVENTORY.json"""
    
    @classmethod
    def setUpClass(cls):
        """Load inventory once for all tests."""
        with open("indices/REPOSITORY_INVENTORY.json") as f:
            cls.inventory = json.load(f)
    
    # Test 1: Inventory not empty
    def test_inventory_not_empty(self):
        """Test that inventory contains repositories."""
        self.assertGreater(len(self.inventory["repositories"]), 0,
                          "Inventory must contain at least one repository")
    
    # Test 2: Statistics present
    def test_statistics_present(self):
        """Test that statistics object exists."""
        self.assertIn("statistics", self.inventory)
        stats = self.inventory["statistics"]
        self.assertIn("total_repositories", stats)
        self.assertIn("archived_count", stats)
        self.assertIn("public_count", stats)
        self.assertIn("private_count", stats)
    
    # Test 3: No duplicate IDs
    def test_no_duplicate_ids(self):
        """Test that no repository IDs are duplicated."""
        ids = [r["repository_id"] for r in self.inventory["repositories"]]
        self.assertEqual(len(ids), len(set(ids)),
                        "Repository IDs must be unique")
    
    # Test 4: No duplicate names
    def test_no_duplicate_names(self):
        """Test that no repository names are duplicated."""
        names = [r["repository_full_name"] for r in self.inventory["repositories"]]
        self.assertEqual(len(names), len(set(names)),
                        "Repository full names must be unique")
    
    # Test 5: Required fields present
    def test_required_fields_present(self):
        """Test that all required fields are present in each repo."""
        required_fields = [
            "repository_full_name",
            "repository_id",
            "owner",
            "repository_name",
            "url",
            "default_branch",
            "visibility",
            "archived",
            "size_bytes",
            "created_at",
            "updated_at",
            "pushed_at",
            "evidence_status"
        ]
        
        for repo in self.inventory["repositories"]:
            for field in required_fields:
                self.assertIn(field, repo,
                            f"Repository {repo.get('repository_full_name', 'UNKNOWN')} missing field: {field}")
    
    # Test 6: Valid visibility values
    def test_valid_visibility_values(self):
        """Test that visibility is either 'public' or 'private'."""
        for repo in self.inventory["repositories"]:
            self.assertIn(repo["visibility"], ["public", "private"],
                         f"Invalid visibility: {repo['visibility']}")
    
    # Test 7: Valid evidence status
    def test_valid_evidence_status(self):
        """Test that evidence_status is one of the allowed marks."""
        allowed_marks = ["FATO", "HIPOTESE", "SIMBOLICO", "LACUNA"]
        for repo in self.inventory["repositories"]:
            self.assertIn(repo["evidence_status"], allowed_marks,
                         f"Invalid evidence_status: {repo['evidence_status']}")
    
    # Test 8: Repository count coherence
    def test_repository_count_coherence(self):
        """Test that total count >= all specific counts."""
        stats = self.inventory["statistics"]
        total = stats["total_repositories"]
        public = stats["public_count"]
        private = stats["private_count"]
        archived = stats["archived_count"]
        
        # Public + Private should equal total (or be subset if partial list)
        self.assertLessEqual(public + private, total,
                            "Public + Private must not exceed total")
    
    # Test 9: GitHub URL format
    def test_github_url_format(self):
        """Test that URLs are valid GitHub URLs."""
        for repo in self.inventory["repositories"]:
            url = repo["url"]
            self.assertTrue(url.startswith("https://github.com/"),
                           f"Invalid GitHub URL: {url}")
    
    # Test 10: Repository ID is integer
    def test_repository_id_is_integer(self):
        """Test that repository_id is a positive integer."""
        for repo in self.inventory["repositories"]:
            self.assertIsInstance(repo["repository_id"], int)
            self.assertGreater(repo["repository_id"], 0,
                              "Repository ID must be positive")
    
    # Test 11: Size bytes is non-negative
    def test_size_bytes_non_negative(self):
        """Test that size_bytes is non-negative."""
        for repo in self.inventory["repositories"]:
            self.assertGreaterEqual(repo["size_bytes"], 0,
                                   f"Invalid size_bytes: {repo['size_bytes']}")
    
    # Test 12: Archived boolean
    def test_archived_is_boolean(self):
        """Test that archived field is boolean."""
        for repo in self.inventory["repositories"]:
            self.assertIsInstance(repo["archived"], bool)
    
    # Test 13: Owner in allowed list
    def test_owner_in_allowed_list(self):
        """Test that all owners are in ALLOWED_OWNERS."""
        allowed_owners = ["rafaelmeloreisnovo", "instituto-Rafael"]
        for repo in self.inventory["repositories"]:
            self.assertIn(repo["owner"], allowed_owners,
                         f"Owner {repo['owner']} not in allowed list")
    
    # Test 14: Full name matches owner/repository_name
    def test_full_name_matches_components(self):
        """Test that repository_full_name matches owner/repository_name."""
        for repo in self.inventory["repositories"]:
            expected = f"{repo['owner']}/{repo['repository_name']}"
            actual = repo["repository_full_name"]
            self.assertEqual(expected, actual,
                            f"Full name mismatch: {expected} != {actual}")
    
    # Test 15: Organizations present in metadata
    def test_organizations_present_in_metadata(self):
        """Test that organizations list is not empty."""
        self.assertIn("organizations", self.inventory)
        self.assertGreater(len(self.inventory["organizations"]), 0,
                          "Organizations list must not be empty")
    
    # Test 16: Generated at timestamp is valid
    def test_generated_at_timestamp_valid(self):
        """Test that generated_at is a valid ISO-8601 timestamp."""
        try:
            from datetime import datetime
            generated_at = self.inventory["generated_at"]
            datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
        except ValueError as e:
            self.fail(f"Invalid generated_at timestamp: {e}")
    
    # Test 17: Inventory source is valid
    def test_inventory_source_valid(self):
        """Test that inventory_source is one of allowed values."""
        allowed_sources = ["github_api", "cache", "manual"]
        self.assertIn(self.inventory["inventory_source"], allowed_sources)
    
    # Test 18: Schema version exists
    def test_schema_version_present(self):
        """Test that schema_version is present and formatted correctly."""
        self.assertIn("schema_version", self.inventory)
        schema_version = self.inventory["schema_version"]
        self.assertTrue(schema_version.startswith("repository_inventory.schema.v"))
    
    # Test 19: Visibility distribution matches stats
    def test_visibility_distribution_matches_stats(self):
        """Test that visibility distribution matches statistics."""
        stats = self.inventory["statistics"]
        public_count = sum(1 for r in self.inventory["repositories"] if r["visibility"] == "public")
        private_count = sum(1 for r in self.inventory["repositories"] if r["visibility"] == "private")
        
        self.assertEqual(public_count, stats["public_count"],
                        "Public count mismatch")
        self.assertEqual(private_count, stats["private_count"],
                        "Private count mismatch")
    
    # Test 20: Archived count matches stats
    def test_archived_count_matches_stats(self):
        """Test that archived count matches statistics."""
        stats = self.inventory["statistics"]
        archived_count = sum(1 for r in self.inventory["repositories"] if r["archived"])
        self.assertEqual(archived_count, stats["archived_count"],
                        "Archived count mismatch")
    
    # Test 21: No TOKEN_VAZIO in critical fields
    def test_no_token_vazio_in_critical_fields(self):
        """Test that TOKEN_VAZIO doesn't appear in critical fields."""
        critical_fields = ["repository_full_name", "repository_id", "url", "owner"]
        for repo in self.inventory["repositories"]:
            for field in critical_fields:
                value = repo.get(field, "")
                self.assertNotIn("TOKEN_VAZIO", str(value),
                                f"TOKEN_VAZIO found in critical field {field}")
    
    # Test 22: Collection method documented
    def test_collection_method_documented(self):
        """Test that collection_method is present."""
        self.assertIn("collection_method", self.inventory)
        self.assertGreater(len(self.inventory["collection_method"]), 0)
    
    # Test 23: Validation status documented
    def test_validation_status_documented(self):
        """Test that validation_status is present."""
        self.assertIn("validation_status", self.inventory)
        allowed_statuses = ["PENDING", "PASS", "FAIL", "PARTIAL"]
        self.assertIn(self.inventory["validation_status"], allowed_statuses)
    
    # Test 24: Sync status valid for all repos
    def test_sync_status_valid_for_all_repos(self):
        """Test that sync_status is valid for all repositories."""
        allowed_statuses = ["CURRENT", "STALE", "NEEDS_REFRESH"]
        for repo in self.inventory["repositories"]:
            self.assertIn(repo.get("sync_status", "CURRENT"), allowed_statuses)
    
    # Test 25: First seen at timestamp present
    def test_first_seen_at_timestamp_present(self):
        """Test that first_seen_at timestamp is present and valid."""
        from datetime import datetime
        for repo in self.inventory["repositories"]:
            self.assertIn("first_seen_at", repo)
            try:
                datetime.fromisoformat(repo["first_seen_at"].replace("Z", "+00:00"))
            except ValueError as e:
                self.fail(f"Invalid first_seen_at in {repo['repository_full_name']}: {e}")

if __name__ == "__main__":
    # Run tests with verbose output
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestRepositoryInventory)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
