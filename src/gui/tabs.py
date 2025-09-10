"""
Tab classes for the WSL Manager GUI.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from .widgets import DistributionTreeView, ActionButtons, SummaryFrame, TabFrame
from .config import INSTALLED_COLUMNS, AVAILABLE_COLUMNS, STYLES


class InstalledTab(TabFrame):
    """Tab for displaying installed WSL distributions."""
    
    def __init__(self, parent, on_refresh: Callable, on_rename: Callable, on_delete: Callable):
        super().__init__(parent)
        self.on_refresh = on_refresh
        self.on_rename = on_rename
        self.on_delete = on_delete
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the installed distributions tab UI."""
        # Create action buttons
        button_configs = {
            'refresh': {
                'text': 'Refresh',
                'command': self.on_refresh
            },
            'rename': {
                'text': 'Rename Selected',
                'command': self.on_rename,
                'state': 'disabled'
            },
            'delete': {
                'text': 'Delete Selected',
                'command': self.on_delete,
                'state': 'disabled'
            }
        }
        
        self.action_buttons = ActionButtons(self, button_configs)
        
        # Set up header
        self.setup_header("Currently Installed WSL Distributions", self.action_buttons)
        
        # Create treeview
        self.treeview = DistributionTreeView(self, INSTALLED_COLUMNS, height=15)
        
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        
        # Set up treeview
        self.setup_treeview(self.treeview, self.scrollbar)
        
        # Bind selection event
        self.treeview.bind('<<TreeviewSelect>>', self.on_selection_change)
        
        # Create summary frame
        self.summary_frame = SummaryFrame(self, "Summary")
        self.setup_summary(self.summary_frame)
    
    def on_selection_change(self, event):
        """Handle treeview selection change."""
        selection = self.treeview.selection()
        if selection:
            self.action_buttons.set_button_state('rename', 'normal')
            self.action_buttons.set_button_state('delete', 'normal')
        else:
            self.action_buttons.set_button_state('rename', 'disabled')
            self.action_buttons.set_button_state('delete', 'disabled')
    
    def get_selected_distribution(self) -> Optional[str]:
        """Get the name of the selected distribution."""
        selection = self.treeview.selection()
        if selection:
            item = selection[0]
            values = self.treeview.item(item, 'values')
            return values[0]  # Name is the first column
        return None
    
    def clear_data(self):
        """Clear all data from the treeview."""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
    
    def add_distribution(self, name: str, state: str, version: str, is_default: bool):
        """Add a distribution to the treeview."""
        default_text = "Yes" if is_default else "No"
        self.treeview.insert('', 'end', values=(name, state, version, default_text))
    
    def set_summary(self, text: str):
        """Set the summary text."""
        self.summary_frame.set_summary(text)


class AvailableTab(TabFrame):
    """Tab for displaying available WSL distributions."""
    
    def __init__(self, parent, on_refresh: Callable, on_install: Callable):
        super().__init__(parent)
        self.on_refresh = on_refresh
        self.on_install = on_install
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the available distributions tab UI."""
        # Create action buttons
        button_configs = {
            'refresh': {
                'text': 'Refresh',
                'command': self.on_refresh
            },
            'install': {
                'text': 'Install Selected',
                'command': self.on_install,
                'state': 'disabled'
            }
        }
        
        self.action_buttons = ActionButtons(self, button_configs)
        
        # Set up header
        self.setup_header("Available WSL Distributions to Install", self.action_buttons)
        
        # Create treeview
        self.treeview = DistributionTreeView(self, AVAILABLE_COLUMNS, height=15)
        
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        
        # Set up treeview
        self.setup_treeview(self.treeview, self.scrollbar)
        
        # Bind selection event
        self.treeview.bind('<<TreeviewSelect>>', self.on_selection_change)
        
        # Create summary frame
        self.summary_frame = SummaryFrame(self, "Summary")
        self.setup_summary(self.summary_frame)
    
    def on_selection_change(self, event):
        """Handle treeview selection change."""
        selection = self.treeview.selection()
        if selection:
            self.action_buttons.set_button_state('install', 'normal')
        else:
            self.action_buttons.set_button_state('install', 'disabled')
    
    def get_selected_distribution(self) -> Optional[tuple]:
        """Get the name and friendly name of the selected distribution."""
        selection = self.treeview.selection()
        if selection:
            item = selection[0]
            values = self.treeview.item(item, 'values')
            return values[0], values[1]  # Name and friendly name
        return None
    
    def clear_data(self):
        """Clear all data from the treeview."""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
    
    def add_distribution(self, name: str, friendly_name: str):
        """Add a distribution to the treeview."""
        install_cmd = f"wsl --install {name}"
        self.treeview.insert('', 'end', values=(name, friendly_name, install_cmd))
    
    def set_summary(self, text: str):
        """Set the summary text."""
        self.summary_frame.set_summary(text)


class ActionsTab(TabFrame):
    """Tab for actions and additional functionality."""
    
    def __init__(self, parent, on_refresh_all: Callable, on_export_json: Callable, on_show_help: Callable):
        super().__init__(parent)
        self.on_refresh_all = on_refresh_all
        self.on_export_json = on_export_json
        self.on_show_help = on_show_help
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the actions tab UI."""
        # Header
        ttk.Label(self, text="WSL Management Actions", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Actions frame
        actions_buttons_frame = ttk.LabelFrame(self, text="Quick Actions", padding="10")
        actions_buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Action buttons with modern styling
        ttk.Button(actions_buttons_frame, text="Refresh All Data", command=self.on_refresh_all, style=STYLES['primary_button']).grid(row=0, column=0, padx=(0, 10), pady=5)
        ttk.Button(actions_buttons_frame, text="Export to JSON", command=self.on_export_json, style=STYLES['success_button']).grid(row=0, column=1, padx=(0, 10), pady=5)
        ttk.Button(actions_buttons_frame, text="Show Help", command=self.on_show_help, style=STYLES['secondary_button']).grid(row=0, column=2, pady=5)
        
        # JSON output frame
        from .widgets import JSONOutputFrame
        self.json_frame = JSONOutputFrame(self)
        self.json_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def set_json_output(self, json_text: str):
        """Set the JSON output text."""
        self.json_frame.set_json(json_text)
