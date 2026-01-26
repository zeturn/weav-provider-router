"""Version bump utility for weav-provider-router."""

import argparse
import re
import subprocess
from pathlib import Path


def get_current_version() -> str:
    """Get current version from pyproject.toml."""
    pyproject = Path("pyproject.toml")
    content = pyproject.read_text(encoding="utf-8")
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)


def bump_version(version: str, bump_type: str) -> str:
    """Bump version number."""
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")
    
    major, minor, patch = map(int, parts)
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")
    
    return f"{major}.{minor}.{patch}"


def update_version_in_file(new_version: str) -> None:
    """Update version in pyproject.toml."""
    pyproject = Path("pyproject.toml")
    content = pyproject.read_text(encoding="utf-8")
    new_content = re.sub(
        r'version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        content
    )
    pyproject.write_text(new_content, encoding="utf-8")


def update_changelog(version: str) -> None:
    """Add entry to CHANGELOG.md."""
    changelog = Path("CHANGELOG.md")
    if not changelog.exists():
        return
    
    content = changelog.read_text(encoding="utf-8")
    
    # Find [Unreleased] section
    unreleased_pattern = r"## \[Unreleased\]"
    if not re.search(unreleased_pattern, content):
        print("Warning: Could not find [Unreleased] section in CHANGELOG.md")
        return
    
    # Add new version section
    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    new_section = f"\n\n## [{version}] - {today}\n\n### Changed\n- Update version to {version}\n"
    
    content = re.sub(
        unreleased_pattern,
        f"## [Unreleased]{new_section}",
        content,
        count=1
    )
    
    changelog.write_text(content, encoding="utf-8")


def create_git_tag(version: str, push: bool = False) -> None:
    """Create git tag for version."""
    tag = f"v{version}"
    
    # Check if tag already exists
    result = subprocess.run(
        ["git", "tag", "-l", tag],
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print(f"Warning: Tag {tag} already exists")
        return
    
    # Create tag
    subprocess.run(["git", "tag", tag], check=True)
    print(f"Created tag: {tag}")
    
    if push:
        subprocess.run(["git", "push", "origin", tag], check=True)
        print(f"Pushed tag: {tag}")


def main():
    parser = argparse.ArgumentParser(description="Bump version for weav-provider-router")
    parser.add_argument(
        "bump_type",
        choices=["major", "minor", "patch"],
        help="Type of version bump"
    )
    parser.add_argument(
        "--no-commit",
        action="store_true",
        help="Don't create git commit"
    )
    parser.add_argument(
        "--no-tag",
        action="store_true",
        help="Don't create git tag"
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push tag to remote"
    )
    
    args = parser.parse_args()
    
    # Get current version
    current = get_current_version()
    print(f"Current version: {current}")
    
    # Bump version
    new_version = bump_version(current, args.bump_type)
    print(f"New version: {new_version}")
    
    # Update files
    print("\nUpdating pyproject.toml...")
    update_version_in_file(new_version)
    
    print("Updating CHANGELOG.md...")
    update_changelog(new_version)
    
    # Git operations
    if not args.no_commit:
        print("\nCreating git commit...")
        subprocess.run(["git", "add", "pyproject.toml", "CHANGELOG.md"], check=True)
        subprocess.run(
            ["git", "commit", "-m", f"Bump version to {new_version}"],
            check=True
        )
        print("Committed changes")
    
    if not args.no_tag:
        print("\nCreating git tag...")
        create_git_tag(new_version, args.push)
    
    print(f"\n✅ Version bumped to {new_version}")
    print("\nNext steps:")
    print("1. Review the changes")
    print("2. Push to remote: git push")
    print(f"3. Push tag: git push origin v{new_version}")
    print("4. Create GitHub release to trigger PyPI publish")


if __name__ == "__main__":
    main()
