#!/usr/bin/env python3
"""
Script to automatically update README.md version badges and references 
based on the package_version in manifest.json
"""

import json
import re
import os
import sys
from pathlib import Path

def get_manifest_version():
    """Extract version from manifest.json"""
    manifest_path = Path("Packages/vikingstudios-airport-lmml-malta/manifest.json")
    
    if not manifest_path.exists():
        print(f"Error: manifest.json not found at {manifest_path}")
        sys.exit(1)
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        version = manifest.get('package_version')
        if not version:
            print("Error: package_version not found in manifest.json")
            sys.exit(1)
            
        return version
    except json.JSONDecodeError as e:
        print(f"Error parsing manifest.json: {e}")
        sys.exit(1)

def update_readme_version(version):
    """Update version references in README.md"""
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        print("Error: README.md not found")
        sys.exit(1)
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update version badge
        content = re.sub(
            r'!\[Version\]\(https://img\.shields\.io/badge/Version-[^)]*-green\)',
            f'![Version](https://img.shields.io/badge/Version-{version}-green)',
            content
        )
        
        # Update "Current Features" heading
        content = re.sub(
            r'### ✅ Current Features \(v[^)]*\)',
            f'### ✅ Current Features (v{version})',
            content
        )
        
        # Update latest version in changelog section
        content = re.sub(
            r'\*\*Latest Version: [^*]*\*\*',
            f'**Latest Version: {version}**',
            content
        )
        
        # Update any other version references in the format "v0.1.3"
        content = re.sub(
            r'\bv\d+\.\d+\.\d+\b',
            f'v{version}',
            content
        )
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated README.md with version {version}")
        return True
        
    except Exception as e:
        print(f"Error updating README.md: {e}")
        return False

def main():
    """Main function"""
    print("🔄 Updating README.md version from manifest.json...")
    
    # Change to script directory and then to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Get version from manifest
    version = get_manifest_version()
    print(f"📦 Found version {version} in manifest.json")
    
    # Update README
    if update_readme_version(version):
        print("🎉 Version update completed successfully!")
    else:
        print("❌ Version update failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
