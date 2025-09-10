#!/usr/bin/env python3
"""
Simple script to create the release package from existing executables.
"""

import shutil
from pathlib import Path

def create_release_package():
    """Create a release package with both executables."""
    print("Creating Release Package...")
    
    release_dir = Path("release")
    if release_dir.exists():
        try:
            shutil.rmtree(release_dir)
            print("✓ Cleaned existing release directory")
        except PermissionError as e:
            print(f"⚠️  Warning: Could not delete existing release directory: {e}")
            print("   This usually happens when executables are being scanned by antivirus software.")
            print("   Trying to copy files anyway...")
    
    release_dir.mkdir(exist_ok=True)
    
    # Copy executables
    cli_exe = Path("dist/WSLManager.exe")
    gui_exe = Path("dist/WSLManagerGUI.exe")
    
    success_count = 0
    
    if cli_exe.exists():
        try:
            shutil.copy2(cli_exe, release_dir / "WSLManager.exe")
            print(f"✓ Copied {cli_exe} to release/")
            success_count += 1
        except PermissionError as e:
            print(f"⚠️  Warning: Could not copy CLI executable: {e}")
            print("   The file may be in use or locked by antivirus software.")
    else:
        print(f"✗ CLI executable not found: {cli_exe}")
    
    if gui_exe.exists():
        try:
            shutil.copy2(gui_exe, release_dir / "WSLManagerGUI.exe")
            print(f"✓ Copied {gui_exe} to release/")
            success_count += 1
        except PermissionError as e:
            print(f"⚠️  Warning: Could not copy GUI executable: {e}")
            print("   The file may be in use or locked by antivirus software.")
    else:
        print(f"✗ GUI executable not found: {gui_exe}")
    
    # Create README for release
    readme_content = """# WSL Manager - Release Package

This package contains standalone executables for the WSL Manager application.

## Files Included

- `WSLManager.exe` - Command-line interface
- `WSLManagerGUI.exe` - Graphical user interface

## Usage

### CLI Version
```bash
WSLManager.exe installed    # Show installed distributions
WSLManager.exe available    # Show available distributions
WSLManager.exe help         # Show help
```

### GUI Version
Double-click `WSLManagerGUI.exe` to launch the graphical interface.

## Requirements

- Windows 10/11
- WSL installed and configured
- No Python installation required

## Support

For issues or questions, please refer to the main project documentation.
"""
    
    readme_path = release_dir / "README.txt"
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✓ Created {readme_path}")
    except Exception as e:
        print(f"⚠️  Warning: Could not create README.txt: {e}")
    
    print(f"\nRelease package creation completed! ({success_count}/2 executables copied)")
    if success_count == 2:
        print("✓ All executables successfully copied to release/ directory")
    else:
        print("⚠️  Some executables could not be copied due to permission issues")
        print("   This is usually caused by antivirus software scanning the files")
        print("   You can manually copy the files from dist/ to release/ if needed")

if __name__ == "__main__":
    create_release_package()
