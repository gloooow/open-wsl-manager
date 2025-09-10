#!/usr/bin/env python3
"""
WSL Manager - Legacy Entry Point

This file provides backward compatibility with the old entry point.
For new installations, use: wsl-manager [command]
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for backward compatibility
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the CLI main function
from wsl_manager.cli.main import main

if __name__ == "__main__":
    main()