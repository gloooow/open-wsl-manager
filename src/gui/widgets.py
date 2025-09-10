"""
Reusable GUI widgets and components.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Callable, Optional, Dict, Any


class DistributionTreeView(ttk.Treeview):
    """Custom TreeView for displaying WSL distributions."""
    
    def __init__(self, parent, columns_config: Dict[str, Any], **kwargs):
        super().__init__(parent, **kwargs)
        self.columns_config = columns_config
        self.setup_columns()
    
    def setup_columns(self):
        """Configure the treeview columns."""
        columns = self.columns_config['columns']
        self.configure(columns=columns, show='headings')
        
        # Set up headings and column widths
        for col in columns:
            self.heading(col, text=self.columns_config['headings'][col])
            self.column(col, width=self.columns_config['widths'][col])


class ActionButtons(ttk.Frame):
    """Frame containing action buttons for distributions."""
    
    def __init__(self, parent, button_configs: Dict[str, Dict[str, Any]], **kwargs):
        super().__init__(parent, **kwargs)
        self.buttons = {}
        self.setup_buttons(button_configs)
    
    def setup_buttons(self, button_configs: Dict[str, Dict[str, Any]]):
        """Create and configure action buttons."""
        for name, config in button_configs.items():
            button = ttk.Button(
                self,
                text=config['text'],
                command=config['command'],
                state=config.get('state', 'normal')
            )
            button.grid(
                row=config.get('row', 0),
                column=config.get('column', 0),
                padx=config.get('padx', (10, 0)),
                pady=config.get('pady', 0)
            )
            self.buttons[name] = button
    
    def get_button(self, name: str) -> ttk.Button:
        """Get a button by name."""
        return self.buttons.get(name)
    
    def set_button_state(self, name: str, state: str):
        """Set the state of a button."""
        if name in self.buttons:
            self.buttons[name].config(state=state)


class StatusBar(ttk.Label):
    """Status bar widget for displaying application status."""
    
    def __init__(self, parent, **kwargs):
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        super().__init__(parent, textvariable=self.status_var, **kwargs)
    
    def set_status(self, message: str):
        """Set the status message."""
        self.status_var.set(message)
    
    def get_status(self) -> str:
        """Get the current status message."""
        return self.status_var.get()


class SummaryFrame(ttk.LabelFrame):
    """Frame for displaying summary information."""
    
    def __init__(self, parent, title: str, **kwargs):
        super().__init__(parent, text=title, padding="5", **kwargs)
        self.summary_var = tk.StringVar()
        self.summary_var.set("No data loaded")
        ttk.Label(self, textvariable=self.summary_var).grid(row=0, column=0, sticky=tk.W)
    
    def set_summary(self, text: str):
        """Set the summary text."""
        self.summary_var.set(text)
    
    def get_summary(self) -> str:
        """Get the current summary text."""
        return self.summary_var.get()


class JSONOutputFrame(ttk.LabelFrame):
    """Frame for displaying JSON output."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="JSON Output", padding="5", **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.json_text = scrolledtext.ScrolledText(self, height=15, width=80)
        self.json_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def set_json(self, json_text: str):
        """Set the JSON text content."""
        self.json_text.delete(1.0, tk.END)
        self.json_text.insert(1.0, json_text)
    
    def get_json(self) -> str:
        """Get the current JSON text content."""
        return self.json_text.get(1.0, tk.END).strip()


class HeaderFrame(ttk.Frame):
    """Header frame with title and action buttons."""
    
    def __init__(self, parent, title: str, buttons: Optional[ActionButtons] = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure(0, weight=1)
        
        # Title label
        ttk.Label(self, text=title, style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        # Action buttons
        if buttons:
            buttons.grid(row=0, column=1, padx=(10, 0))


class TabFrame(ttk.Frame):
    """Base frame for tab content."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, padding="10", **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
    
    def setup_header(self, title: str, buttons: Optional[ActionButtons] = None):
        """Set up the header with title and buttons."""
        header = HeaderFrame(self, title, buttons)
        header.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        return header
    
    def setup_treeview(self, treeview: DistributionTreeView, scrollbar: ttk.Scrollbar):
        """Set up treeview with scrollbar."""
        treeview.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
    
    def setup_summary(self, summary_frame: SummaryFrame):
        """Set up the summary frame."""
        summary_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
