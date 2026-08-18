#!/usr/bin/env python3
"""
Bulk update GitHub Actions refs in workflows from version tags to pinned SHAs.

Scans all .github/workflows/*.yml files, identifies version-tagged actions,
resolves them to commit SHAs via GitHub API, and updates files in-place.
Maintains append-only audit trail of all migrations.
"""

import argparse
import json
import os
import re
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime, timezone

# Import resolver from sibling module
sys.path.insert(0, str(Path(__file__).parent))
from resolve_action_shas import resolve_action_sha


def find_workflow_files(workflows_dir: Path) -> List[Path]:
    """Find all .yml workflow files in .github/workflows/"""
    if not workflows_dir.exists():
        return []
    return sorted(workflows_dir.glob("*.yml"))


def find_action_refs(content: str) -> List[Tuple[str, int]]:
    """
    Find all 'uses:' action references in workflow YAML.

    Returns: List of (action_ref, line_number) tuples
    """
    matches = []
    # Match pattern: uses: owner/repo@version or uses: owner/repo@ref (may have quotes)
    pattern = r'^\s*uses:\s*["\']?([a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+@[^\s"\']+)["\']?'

    for line_num, line in enumerate(content.split("\n"), start=1):
        m = re.match(pattern, line)
        if m:
            action_ref = m.group(1)
            # Skip if already a SHA (40 hex chars)
            parts = action_ref.split("@")
            if len(parts) == 2:
                version = parts[1]
                if not (len(version) == 40 and all(c in "0123456789abcdef" for c in version.lower())):
                    matches.append((action_ref, line_num))

    return matches


def update_workflow_content(
    content: str,
    migrations: Dict[str, str]  # {old_ref: new_ref}
) -> Tuple[str, int]:
    """
    Replace version-tagged action refs with pinned SHAs.

    Returns: (updated_content, num_replacements)
    """
    updated = content
    count = 0

    for old_ref, new_ref in migrations.items():
        # Replace in uses: directive - handle both quoted and unquoted
        patterns = [
            f"uses: {old_ref}",
            f'uses: "{old_ref}"',
            f"uses: '{old_ref}'",
        ]

        for pattern in patterns:
            if pattern in updated:
                replacement = pattern.replace(old_ref, new_ref)
                updated = updated.replace(pattern, replacement)
                count += 1

    return updated, count


def log_migration(
    audit_path: Path,
    workflow_file: str,
    action_ref: str,
    new_sha: str,
    status: str = "SUCCESS"
):
    """Append migration record to audit trail (append-only)."""
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {
        "timestamp": timestamp,
        "workflow_file": workflow_file,
        "action_ref": action_ref,
        "new_sha": new_sha,
        "status": status,
    }

    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with open(audit_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Bulk pin GitHub Actions in workflows to commit SHAs"
    )
    p.add_argument(
        "--repo-root",
        default="/home/user/Mapa",
        help="Repository root directory"
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes; default is dry-run"
    )
    p.add_argument(
        "--token-env",
        default="GITHUB_TOKEN",
        help="Environment variable containing GitHub token"
    )
    ns = p.parse_args(argv)

    repo_root = Path(ns.repo_root)
    workflows_dir = repo_root / ".github" / "workflows"
    audit_path = repo_root / "data" / "audits" / "action-pinning-audit.jsonl"

    if not workflows_dir.exists():
        print(f"ERROR: workflows directory not found: {workflows_dir}")
        return 1

    token = os.environ.get(ns.token_env, "").strip()
    if not token:
        print(f"REJECT missing token in {ns.token_env}")
        return 2

    # Find all workflow files
    workflow_files = find_workflow_files(workflows_dir)
    print(f"Found {len(workflow_files)} workflow files")

    total_actions = 0
    total_migrations = 0
    failed_resolutions = 0

    for workflow_file in workflow_files:
        content = workflow_file.read_text(encoding="utf-8")
        action_refs = find_action_refs(content)

        if not action_refs:
            continue

        print(f"\n{workflow_file.name}: {len(action_refs)} version-tagged action(s)")
        migrations = {}

        for action_ref, line_num in action_refs:
            total_actions += 1
            print(f"  Line {line_num}: {action_ref}", end=" → ")

            # Resolve to SHA
            sha = resolve_action_sha(action_ref, token)
            if not sha:
                print("FAILED")
                log_migration(
                    audit_path,
                    workflow_file.name,
                    action_ref,
                    "",
                    status="FAILED_RESOLUTION"
                )
                failed_resolutions += 1
                continue

            print(f"{sha[:8]}...")
            migrations[action_ref] = sha.lower()
            total_migrations += 1
            log_migration(
                audit_path,
                workflow_file.name,
                action_ref,
                sha,
                status="SUCCESS"
            )

        # Apply migrations to file
        if migrations:
            updated_content, count = update_workflow_content(content, migrations)
            if count > 0:
                if ns.apply:
                    workflow_file.write_text(updated_content, encoding="utf-8")
                    print(f"  ✓ Updated {count} reference(s)")
                else:
                    print(f"  [DRY-RUN] Would update {count} reference(s)")

    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total workflow files: {len(workflow_files)}")
    print(f"  Total version-tagged actions: {total_actions}")
    print(f"  Successfully resolved: {total_migrations}")
    print(f"  Failed resolutions: {failed_resolutions}")
    print(f"  Audit trail: {audit_path}")

    if not ns.apply:
        print(f"\n[DRY-RUN] No changes applied. Use --apply to update workflows.")

    if failed_resolutions > 0:
        print(f"\nWARNING: {failed_resolutions} actions failed to resolve. Check audit trail.")
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
