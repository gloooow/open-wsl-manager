"""
Main window class for the WSL Manager GUI.
"""

import tkinter as tk
from tkinter import ttk
from .config import WINDOW_TITLE, WINDOW_SIZE, MIN_WINDOW_SIZE, STYLES, FONTS
from .tabs import InstalledTab, AvailableTab, ActionsTab
from .widgets import StatusBar
from .actions import WSLManagerActions
from .models import DistributionViewModel, TabState


class WSLManagerGUI:
    """Main GUI application for WSL Manager."""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(*MIN_WINDOW_SIZE)
        
        # Initialize data models
        self.view_model = DistributionViewModel()
        self.tab_state = TabState()
        
        # Initialize actions handler
        self.actions = WSLManagerActions(self.set_status)
        
        # Configure style
        self.setup_styles()
        
        # Create main interface
        self.create_widgets()
        
        # Load initial data
        self.refresh_data()
    
    def setup_styles(self):
        """Configure the application styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure(STYLES['title'], font=FONTS['title'])
        style.configure(STYLES['header'], font=FONTS['header'])
        style.configure(STYLES['status'], font=FONTS['status'])
        
        # Configure treeview
        style.configure('Treeview', rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """Create the main GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text=WINDOW_TITLE, style=STYLES['title'])
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_tabs()
        
        # Status bar
        self.status_bar = StatusBar(main_frame, style=STYLES['status'])
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_tabs(self):
        """Create the application tabs."""
        # Installed distributions tab
        self.installed_tab = InstalledTab(
            self.notebook,
            on_refresh=self.refresh_installed,
            on_rename=self.rename_selected_distribution,
            on_delete=self.delete_selected_distribution
        )
        self.notebook.add(self.installed_tab, text="Installed Distributions")
        
        # Available distributions tab
        self.available_tab = AvailableTab(
            self.notebook,
            on_refresh=self.refresh_available,
            on_install=self.install_selected_distribution
        )
        self.notebook.add(self.available_tab, text="Available Distributions")
        
        # Actions tab
        self.actions_tab = ActionsTab(
            self.notebook,
            on_refresh_all=self.refresh_data,
            on_export_json=self.export_to_json,
            on_show_help=self.show_help
        )
        self.notebook.add(self.actions_tab, text="Actions & Info")
    
    def set_status(self, message: str):
        """Set the status bar message."""
        self.status_bar.set_status(message)
    
    def refresh_installed(self):
        """Refresh installed distributions data."""
        def update_ui(distributions, summary):
            # Update view model
            self.view_model.update_installed(distributions)
            
            # Clear existing data
            self.installed_tab.clear_data()
            
            # Add new data
            for dist in distributions:
                self.installed_tab.add_distribution(dist.name, dist.state, dist.version, dist.is_default)
            
            # Update summary
            self.installed_tab.set_summary(summary)
        
        self.actions.refresh_installed_distributions(update_ui)
    
    def refresh_available(self):
        """Refresh available distributions data."""
        def update_ui(distributions, summary):
            # Update view model
            self.view_model.update_available(distributions)
            
            # Clear existing data
            self.available_tab.clear_data()
            
            # Add new data
            for dist in distributions:
                self.available_tab.add_distribution(dist.name, dist.friendly_name)
            
            # Update summary
            self.available_tab.set_summary(summary)
        
        self.actions.refresh_available_distributions(update_ui)
    
    def refresh_data(self):
        """Refresh all data."""
        self.refresh_installed()
        self.refresh_available()
    
    def export_to_json(self):
        """Export data to JSON format."""
        def update_ui(json_output):
            self.actions_tab.set_json_output(json_output)
        
        self.actions.export_to_json(update_ui)
    
    def show_help(self):
        """Show help dialog."""
        self.actions.show_help_dialog(self.root)
    
    def delete_selected_distribution(self):
        """Delete the selected WSL distribution."""
        dist_name = self.installed_tab.get_selected_distribution()
        if not dist_name:
            self.actions.show_warning("No Selection", "Please select a distribution to delete.")
            return
        
        # Show confirmation dialog
        result = self.actions.confirm_action(
            "Confirm Deletion",
            f"Are you sure you want to delete the WSL distribution '{dist_name}'?\n\n"
            "This action cannot be undone and will permanently remove the distribution and all its data.",
            'warning'
        )
        
        if result:
            self.actions.delete_distribution(dist_name, self.refresh_installed)
    
    def rename_selected_distribution(self):
        """Rename the selected WSL distribution."""
        dist_name = self.installed_tab.get_selected_distribution()
        if not dist_name:
            self.actions.show_warning("No Selection", "Please select a distribution to rename.")
            return
        
        # Show rename dialog
        new_name = self.actions.show_rename_dialog(self.root, dist_name)
        if new_name is None:  # User cancelled
            return
        
        # Show confirmation dialog
        result = self.actions.confirm_action(
            "Confirm Rename",
            f"Are you sure you want to rename '{dist_name}' to '{new_name}'?\n\n"
            "This will export and re-import the distribution, which may take a few minutes.",
            'question'
        )
        
        if result:
            self.actions.rename_distribution(dist_name, new_name, self.refresh_installed)
    
    def install_selected_distribution(self):
        """Install the selected WSL distribution with optional custom name."""
        selection = self.available_tab.get_selected_distribution()
        if not selection:
            self.actions.show_warning("No Selection", "Please select a distribution to install.")
            return
        
        dist_name, friendly_name = selection
        
        # Show custom name dialog
        custom_name = self.actions.show_install_dialog(self.root, dist_name, friendly_name)
        if custom_name is None:  # User cancelled
            return
        
        # Show confirmation dialog
        if custom_name:
            confirm_msg = f"Install '{friendly_name}' with custom name '{custom_name}'?"
        else:
            confirm_msg = f"Install '{friendly_name}' with default name '{dist_name}'?"
        
        result = self.actions.confirm_action(
            "Confirm Installation",
            f"{confirm_msg}\n\nThis will download and install the distribution. This may take several minutes.",
            'question'
        )
        
        if result:
            def refresh_both():
                self.refresh_installed()
                self.refresh_available()
            
            self.actions.install_distribution(dist_name, friendly_name, custom_name, refresh_both)
