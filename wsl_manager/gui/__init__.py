"""
Graphical user interface for WSL Manager.

This module provides the GUI components for managing WSL distributions.
"""

from .main_window import WSLManagerGUI

__all__ = ["WSLManagerGUI"]


def main():
    """Main function to run the GUI application."""
    import tkinter as tk
    from .main_window import WSLManagerGUI
    
    root = tk.Tk()
    app = WSLManagerGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()