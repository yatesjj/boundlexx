#!/usr/bin/env python3
"""
Pre-commit hook to enforce Boundlexx documentation governance standards.
Prevents documentation sprawl and maintains Master Manual hierarchy.
"""

import os
import sys
import re
from pathlib import Path

# Allowed documentation directories
ALLOWED_DOC_DIRS = {
    'docs/manual/',
    'docs/modernization/',
}

# Allowed Master Manual subdirectories
ALLOWED_MANUAL_DIRS = {
    'docs/manual/getting-started/',
    'docs/manual/workflows/',
    'docs/manual/architecture/',
    'docs/manual/migration/',
    'docs/manual/reference/',
    'docs/manual/appendices/',
}

# Files that are always allowed
ALLOWED_ROOT_FILES = {
    'README.md',
    'CHANGELOG.md',
    'CONTRIBUTORS.txt',
    'LICENSE',
}

def check_documentation_governance():
    """Check all staged files for documentation governance violations."""
    violations = []

    # Get list of staged files
    staged_files = os.popen('git diff --cached --name-only').read().strip().split('\n')

    for file_path in staged_files:
        if not file_path:
            continue

        # Check markdown files
        if file_path.endswith('.md'):
            if file_path in ALLOWED_ROOT_FILES:
                continue

            # Check if in allowed documentation directories
            allowed = False
            for allowed_dir in ALLOWED_DOC_DIRS:
                if file_path.startswith(allowed_dir):
                    allowed = True
                    break

            if not allowed:
                violations.append(f"❌ GOVERNANCE VIOLATION: {file_path}")
                violations.append(f"   Markdown files must be in: {', '.join(ALLOWED_DOC_DIRS)}")
                violations.append(f"   Or be a standard root file: {', '.join(ALLOWED_ROOT_FILES)}")
                violations.append("")

        # Check Master Manual hierarchy
        if file_path.startswith('docs/manual/'):
            # Must be in allowed subdirectory or root index
            if file_path == 'docs/manual/index.md':
                continue

            allowed = False
            for allowed_dir in ALLOWED_MANUAL_DIRS:
                if file_path.startswith(allowed_dir):
                    allowed = True
                    break

            if not allowed:
                violations.append(f"❌ MASTER MANUAL VIOLATION: {file_path}")
                violations.append(f"   Files must be in allowed subdirectories:")
                for allowed_dir in sorted(ALLOWED_MANUAL_DIRS):
                    violations.append(f"   - {allowed_dir}")
                violations.append("")

        # Check for root directory pollution
        if '/' not in file_path and file_path not in ALLOWED_ROOT_FILES:
            # Check if it's a known allowed root file pattern
            root_patterns = [
                r'manage\.py',
                r'setup\.py',
                r'pyproject\.toml',
                r'setup\.cfg',
                r'docker-compose.*\.yml',
                r'\.env.*',
                r'.*\.code-workspace',
                r'setup_containers\.py',  # Our setup script
            ]

            allowed_root = False
            for pattern in root_patterns:
                if re.match(pattern, file_path):
                    allowed_root = True
                    break

            if not allowed_root:
                violations.append(f"❌ ROOT POLLUTION: {file_path}")
                violations.append(f"   Root directory files require explicit approval")
                violations.append(f"   Consider: scripts/utilities/, config/, or appropriate subdirectory")
                violations.append("")

    if violations:
        print("🚨 BOUNDLEXX GOVERNANCE VIOLATIONS DETECTED:")
        print("=" * 60)
        for violation in violations:
            print(violation)

        print("📚 GOVERNANCE STANDARDS:")
        print("• ALL documentation goes in docs/manual/ (Master Manual hierarchy)")
        print("• Technical tracking goes in docs/modernization/")
        print("• Scripts go in scripts/utilities/")
        print("• Root directory requires explicit approval")
        print("• See docs/manual/appendices/contributing.md for full guidelines")
        print("")
        print("🔧 TO FIX:")
        print("• Move files to appropriate directories")
        print("• Update Master Manual if adding new documentation")
        print("• Get approval for root directory changes")
        print("")
        return False

    return True

if __name__ == "__main__":
    if not check_documentation_governance():
        sys.exit(1)
    print("✅ Documentation governance check passed")
