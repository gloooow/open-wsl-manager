#!/usr/bin/env python3
"""
WSL Manager GUI

A graphical user interface for managing WSL distributions.
"""

import tkinter as tk
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.gui.main_window import WSLManagerGUI


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = WSLManagerGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
