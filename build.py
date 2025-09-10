#!/usr/bin/env python3
"""
Build script for WSL Manager executables

This script automates the process of creating standalone executables
for both the CLI and GUI versions of the WSL Manager application.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    try:
        # Use CREATE_NO_WINDOW on Windows to suppress console windows
        kwargs = {}
        if sys.platform == "win32":
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True, **kwargs)
        print("✓ Success!")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error:", e.stderr)
        return False


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} is installed")
        return True
    except ImportError:
        print("✗ PyInstaller is not installed")
        return False


def install_pyinstaller():
    """Install PyInstaller."""
    print("\nInstalling PyInstaller...")
    return run_command("pip install pyinstaller", "Installing PyInstaller")


def clean_build_dirs():
    """Clean previous build directories."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name} directory...")
            shutil.rmtree(dir_name)
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))


def check_icon_file():
    """Check if icon file exists and warn if not."""
    icon_path = Path("icon.ico")
    if not icon_path.exists():
        print("⚠️  Warning: icon.ico not found")
        print("   Your executables will use the default Python icon")
        print("   To add a custom icon:")
        print("   1. Create or obtain a .ico file")
        print("   2. Save it as 'icon.ico' in the project root")
        print("   3. Rebuild the executables")
        return False
    else:
        print(f"✓ Found icon file: {icon_path}")
        return True


def build_cli():
    """Build the CLI executable."""
    print("\n" + "="*60)
    print("Building CLI Executable")
    print("="*60)
    
    check_icon_file()
    
    command = "pyinstaller wsl_manager_cli.spec"
    return run_command(command, "Building CLI executable")


def build_gui():
    """Build the GUI executable."""
    print("\n" + "="*60)
    print("Building GUI Executable")
    print("="*60)
    
    check_icon_file()
    
    command = "pyinstaller wsl_manager_gui.spec"
    return run_command(command, "Building GUI executable")


def create_release_package():
    """Create a release package with both executables."""
    print("\n" + "="*60)
    print("Creating Release Package")
    print("="*60)
    
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir()
    
    # Copy executables
    cli_exe = Path("dist/WSLManager.exe")
    gui_exe = Path("dist/WSLManagerGUI.exe")
    
    if cli_exe.exists():
        shutil.copy2(cli_exe, release_dir / "WSLManager.exe")
        print(f"✓ Copied {cli_exe} to release/")
    else:
        print(f"✗ CLI executable not found: {cli_exe}")
    
    if gui_exe.exists():
        shutil.copy2(gui_exe, release_dir / "WSLManagerGUI.exe")
        print(f"✓ Copied {gui_exe} to release/")
    else:
        print(f"✗ GUI executable not found: {gui_exe}")
    
    # Create README for release
    readme_content = """# WSL Manager - Release Package

This package contains standalone executables for the WSL Manager application.

## Files

- `WSLManager.exe` - Command-line interface for WSL management
- `WSLManagerGUI.exe` - Graphical user interface for WSL management

## Usage

### Command Line Interface
```
WSLManager.exe installed    # Show installed distributions
WSLManager.exe available    # Show available distributions
WSLManager.exe help         # Show help
```

### Graphical Interface
Simply double-click `WSLManagerGUI.exe` to launch the graphical interface.

## Requirements

- Windows 10/11 with WSL installed
- No additional Python installation required

## Notes

These executables are standalone and include all necessary dependencies.
They should work on any Windows system with WSL support.
"""
    
    with open(release_dir / "README.txt", "w") as f:
        f.write(readme_content)
    
    print("✓ Created release README.txt")
    print(f"✓ Release package created in: {release_dir.absolute()}")


def main():
    """Main build function."""
    print("WSL Manager - Executable Builder")
    print("="*60)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py") or not os.path.exists("gui.py"):
        print("✗ Error: Please run this script from the project root directory")
        print("Required files: main.py, gui.py")
        sys.exit(1)
    
    # Check/install PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("✗ Failed to install PyInstaller")
            sys.exit(1)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executables
    cli_success = build_cli()
    gui_success = build_gui()
    
    if not cli_success and not gui_success:
        print("\n✗ All builds failed!")
        sys.exit(1)
    
    # Create release package
    create_release_package()
    
    print("\n" + "="*60)
    print("Build Complete!")
    print("="*60)
    
    if cli_success:
        print("✓ CLI executable: dist/WSLManager.exe")
    if gui_success:
        print("✓ GUI executable: dist/WSLManagerGUI.exe")
    
    print("✓ Release package: release/")
    print("\nYou can now distribute the files from the 'release' directory.")


if __name__ == "__main__":
    main()
