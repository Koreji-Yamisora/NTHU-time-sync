#!/usr/bin/env python3
"""
Script to create a new release tag and push it to trigger the GitHub Actions build.
Usage: python create_release.py <version>
Example: python create_release.py 1.0.0
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python create_release.py <version>")
        print("Example: python create_release.py 1.0.0")
        sys.exit(1)
    
    version = sys.argv[1]
    tag_name = f"v{version}"
    
    print(f"Creating release {tag_name}...")
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("Error: Not in a git repository")
        sys.exit(1)
    
    # Check if tag already exists
    try:
        run_command(f"git rev-parse {tag_name}")
        print(f"Error: Tag {tag_name} already exists")
        sys.exit(1)
    except subprocess.CalledProcessError:
        # Tag doesn't exist, which is what we want
        pass
    
    # Make sure we're on main branch
    current_branch = run_command("git branch --show-current")
    if current_branch != "main":
        print(f"Warning: You're on branch '{current_branch}', not 'main'")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Aborted")
            sys.exit(1)
    
    # Check if there are uncommitted changes
    status = run_command("git status --porcelain")
    if status:
        print("Warning: You have uncommitted changes:")
        print(status)
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Aborted")
            sys.exit(1)
    
    # Create and push the tag
    print(f"Creating tag {tag_name}...")
    run_command(f"git tag {tag_name}")
    
    print(f"Pushing tag {tag_name} to origin...")
    run_command(f"git push origin {tag_name}")
    
    print(f"✅ Release {tag_name} created and pushed!")
    print(f"GitHub Actions will now build the executables for Windows and macOS.")
    print(f"You can monitor the build progress at: https://github.com/YOUR_USERNAME/YOUR_REPO/actions")

if __name__ == "__main__":
    main()
