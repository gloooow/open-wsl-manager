#!/usr/bin/env python3
"""
WSL Manager GUI Launcher - Legacy Entry Point

This file provides backward compatibility with the old GUI launcher.
For new installations, use: wsl-manager-gui
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for backward compatibility
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Launch the GUI application."""
    try:
        # Import and run the GUI
        from wsl_manager.gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error: {e}")
        print("Make sure you're running this from the project root directory.")
        print("Required files: wsl_manager package")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()