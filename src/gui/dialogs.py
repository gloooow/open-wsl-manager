"""
Dialog classes for the WSL Manager GUI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, Any
from .config import DIALOG_CONFIGS, FONTS


class BaseDialog:
    """Base class for modal dialogs."""
    
    def __init__(self, parent, title: str, size: str):
        self.parent = parent
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry(size)
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.dialog, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
    def center_dialog(self):
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def create_buttons_frame(self, buttons_config: list):
        """Create a frame with buttons."""
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        for i, config in enumerate(buttons_config):
            button = ttk.Button(
                buttons_frame,
                text=config['text'],
                command=config['command']
            )
            button.pack(side=tk.RIGHT, padx=(5, 0) if i > 0 else (0, 0))
        
        return buttons_frame
    
    def show(self) -> Optional[Any]:
        """Show the dialog and return the result."""
        self.dialog.wait_window()
        return self.result


class RenameDialog(BaseDialog):
    """Dialog for renaming WSL distributions."""
    
    def __init__(self, parent, current_name: str):
        super().__init__(parent, DIALOG_CONFIGS['rename']['title'], DIALOG_CONFIGS['rename']['size'])
        self.current_name = current_name
        self.setup_dialog()
    
    def setup_dialog(self):
        """Set up the rename dialog."""
        # Title
        title_label = ttk.Label(self.main_frame, text=f"Rename {self.current_name}", style='Header.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Current name label
        current_label = ttk.Label(self.main_frame, text=f"Current name: {self.current_name}")
        current_label.pack(pady=(0, 10))
        
        # New name frame
        name_frame = ttk.Frame(self.main_frame)
        name_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(name_frame, text="New name:").pack(anchor=tk.W)
        self.new_name_var = tk.StringVar()
        self.new_name_entry = ttk.Entry(name_frame, textvariable=self.new_name_var, width=30)
        self.new_name_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Help text
        help_label = ttk.Label(name_frame, text="Name can only contain letters, numbers, hyphens, and underscores", font=FONTS['help'])
        help_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Note about rename process
        note_label = ttk.Label(name_frame, text="Note: Renaming uses export/import process (may take a few minutes)", font=FONTS['help'], foreground='gray')
        note_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Buttons
        buttons_config = [
            {'text': 'Rename', 'command': self.on_rename},
            {'text': 'Cancel', 'command': self.on_cancel}
        ]
        self.create_buttons_frame(buttons_config)
        
        # Focus on the entry field
        self.new_name_entry.focus()
        
        # Handle Enter key
        self.new_name_entry.bind('<Return>', lambda e: self.on_rename())
    
    def on_rename(self):
        """Handle rename button click."""
        new_name = self.new_name_var.get().strip()
        if not new_name:
            messagebox.showerror("Invalid Name", "Please enter a new name.")
            return
        
        if new_name == self.current_name:
            messagebox.showerror("Invalid Name", "New name must be different from current name.")
            return
        
        # Validate new name (basic validation)
        if not new_name.replace('-', '').replace('_', '').isalnum():
            messagebox.showerror("Invalid Name", "New name can only contain letters, numbers, hyphens, and underscores.")
            return
        
        self.result = new_name
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle cancel button click."""
        self.result = None
        self.dialog.destroy()


class InstallDialog(BaseDialog):
    """Dialog for installing WSL distributions with custom names."""
    
    def __init__(self, parent, dist_name: str, friendly_name: str):
        super().__init__(parent, DIALOG_CONFIGS['install']['title'], DIALOG_CONFIGS['install']['size'])
        self.dist_name = dist_name
        self.friendly_name = friendly_name
        self.setup_dialog()
    
    def setup_dialog(self):
        """Set up the install dialog."""
        # Title
        title_label = ttk.Label(self.main_frame, text=f"Install {self.friendly_name}", style='Header.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Info label
        info_label = ttk.Label(self.main_frame, text=f"Distribution: {self.dist_name}")
        info_label.pack(pady=(0, 10))
        
        # Custom name frame
        name_frame = ttk.Frame(self.main_frame)
        name_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(name_frame, text="Custom Name (optional):").pack(anchor=tk.W)
        self.custom_name_var = tk.StringVar()
        self.custom_name_entry = ttk.Entry(name_frame, textvariable=self.custom_name_var, width=30)
        self.custom_name_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Help text
        help_label = ttk.Label(name_frame, text="Leave empty to use default name", font=FONTS['help'])
        help_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Note about custom naming process
        note_label = ttk.Label(name_frame, text="Note: Custom naming uses export/import process (may take longer)", font=FONTS['help'], foreground='gray')
        note_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Buttons
        buttons_config = [
            {'text': 'Install', 'command': self.on_install},
            {'text': 'Cancel', 'command': self.on_cancel}
        ]
        self.create_buttons_frame(buttons_config)
        
        # Focus on the entry field
        self.custom_name_entry.focus()
        
        # Handle Enter key
        self.custom_name_entry.bind('<Return>', lambda e: self.on_install())
    
    def on_install(self):
        """Handle install button click."""
        custom_name = self.custom_name_var.get().strip()
        if custom_name:
            # Validate custom name (basic validation)
            if not custom_name.replace('-', '').replace('_', '').isalnum():
                messagebox.showerror("Invalid Name", "Custom name can only contain letters, numbers, hyphens, and underscores.")
                return
            self.result = custom_name
        else:
            self.result = ""  # Empty string means use default
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle cancel button click."""
        self.result = None
        self.dialog.destroy()


class HelpDialog:
    """Help dialog for the application."""
    
    def __init__(self, parent):
        self.parent = parent
    
    def show(self):
        """Show the help dialog."""
        from .config import HELP_TEXT
        messagebox.showinfo("WSL Manager Help", HELP_TEXT)
