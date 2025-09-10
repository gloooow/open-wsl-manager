#!/usr/bin/env python3
"""
WSL Manager GUI Launcher

Simple launcher script for the WSL Manager GUI application.
"""

import sys
import os
from pathlib import Path

def main():
    """Launch the GUI application."""
    try:
        # Import and run the GUI
        import gui
        gui.main()
    except ImportError as e:
        print(f"Error: {e}")
        print("Make sure you're running this from the project root directory.")
        print("Required files: gui.py, src/wsl_parser.py, src/wsl_online_parser.py")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
