#!/usr/bin/env python3
"""
WSL Manager GUI

A graphical user interface for managing WSL distributions.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
from pathlib import Path
import threading
import json

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.wsl_parser import WSLParser, WSLDistribution
from src.wsl_online_parser import WSLOnlineParser, WSLOnlineDistribution


class WSLManagerGUI:
    """Main GUI application for WSL Manager."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Open WSL Manager")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
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
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 10))
        
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
        title_label = ttk.Label(main_frame, text="Open WSL Manager", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_installed_tab()
        self.create_available_tab()
        self.create_actions_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, style='Status.TLabel')
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_installed_tab(self):
        """Create the installed distributions tab."""
        installed_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(installed_frame, text="Installed Distributions")
        
        # Configure grid
        installed_frame.columnconfigure(0, weight=1)
        installed_frame.rowconfigure(1, weight=1)
        
        # Header with refresh and delete buttons
        header_frame = ttk.Frame(installed_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        
        ttk.Label(header_frame, text="Currently Installed WSL Distributions", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        ttk.Button(header_frame, text="Refresh", command=self.refresh_installed).grid(row=0, column=1, padx=(10, 0))
        self.rename_button = ttk.Button(header_frame, text="Rename Selected", command=self.rename_selected_distribution, state='disabled')
        self.rename_button.grid(row=0, column=2, padx=(10, 0))
        self.delete_button = ttk.Button(header_frame, text="Delete Selected", command=self.delete_selected_distribution, state='disabled')
        self.delete_button.grid(row=0, column=3, padx=(10, 0))
        
        # Treeview for installed distributions
        columns = ('Name', 'State', 'Version', 'Default')
        self.installed_tree = ttk.Treeview(installed_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.installed_tree.heading('Name', text='Distribution Name')
        self.installed_tree.heading('State', text='State')
        self.installed_tree.heading('Version', text='WSL Version')
        self.installed_tree.heading('Default', text='Default')
        
        self.installed_tree.column('Name', width=200)
        self.installed_tree.column('State', width=100)
        self.installed_tree.column('Version', width=100)
        self.installed_tree.column('Default', width=80)
        
        # Scrollbar for treeview
        installed_scrollbar = ttk.Scrollbar(installed_frame, orient=tk.VERTICAL, command=self.installed_tree.yview)
        self.installed_tree.configure(yscrollcommand=installed_scrollbar.set)
        
        self.installed_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        installed_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Bind selection event to enable/disable delete button
        self.installed_tree.bind('<<TreeviewSelect>>', self.on_distribution_select)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(installed_frame, text="Summary", padding="5")
        summary_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.installed_summary_var = tk.StringVar()
        self.installed_summary_var.set("No data loaded")
        ttk.Label(summary_frame, textvariable=self.installed_summary_var).grid(row=0, column=0, sticky=tk.W)
    
    def create_available_tab(self):
        """Create the available distributions tab."""
        available_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(available_frame, text="Available Distributions")
        
        # Configure grid
        available_frame.columnconfigure(0, weight=1)
        available_frame.rowconfigure(1, weight=1)
        
        # Header with refresh and install buttons
        header_frame = ttk.Frame(available_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        
        ttk.Label(header_frame, text="Available WSL Distributions to Install", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        ttk.Button(header_frame, text="Refresh", command=self.refresh_available).grid(row=0, column=1, padx=(10, 0))
        self.install_button = ttk.Button(header_frame, text="Install Selected", command=self.install_selected_distribution, state='disabled')
        self.install_button.grid(row=0, column=2, padx=(10, 0))
        
        # Treeview for available distributions
        columns = ('Name', 'Friendly Name', 'Install Command')
        self.available_tree = ttk.Treeview(available_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.available_tree.heading('Name', text='Distribution Name')
        self.available_tree.heading('Friendly Name', text='Friendly Name')
        self.available_tree.heading('Install Command', text='Install Command')
        
        self.available_tree.column('Name', width=200)
        self.available_tree.column('Friendly Name', width=250)
        self.available_tree.column('Install Command', width=200)
        
        # Scrollbar for treeview
        available_scrollbar = ttk.Scrollbar(available_frame, orient=tk.VERTICAL, command=self.available_tree.yview)
        self.available_tree.configure(yscrollcommand=available_scrollbar.set)
        
        self.available_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        available_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Bind selection event to enable/disable install button
        self.available_tree.bind('<<TreeviewSelect>>', self.on_available_distribution_select)
        

        # Summary frame
        summary_frame = ttk.LabelFrame(available_frame, text="Summary", padding="5")
        summary_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.available_summary_var = tk.StringVar()
        self.available_summary_var.set("No data loaded")
        ttk.Label(summary_frame, textvariable=self.available_summary_var).grid(row=0, column=0, sticky=tk.W)
    
    def create_actions_tab(self):
        """Create the actions tab with additional functionality."""
        actions_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(actions_frame, text="Actions & Info")
        
        # Configure grid
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.rowconfigure(1, weight=1)
        
        # Header
        ttk.Label(actions_frame, text="WSL Management Actions", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Actions frame
        actions_buttons_frame = ttk.LabelFrame(actions_frame, text="Quick Actions", padding="10")
        actions_buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        ttk.Button(actions_buttons_frame, text="Refresh All Data", command=self.refresh_data).grid(row=0, column=0, padx=(0, 10), pady=5)
        ttk.Button(actions_buttons_frame, text="Export to JSON", command=self.export_to_json).grid(row=0, column=1, padx=(0, 10), pady=5)
        ttk.Button(actions_buttons_frame, text="Show Help", command=self.show_help).grid(row=0, column=2, pady=5)
        
        # JSON output frame
        json_frame = ttk.LabelFrame(actions_frame, text="JSON Output", padding="5")
        json_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        json_frame.columnconfigure(0, weight=1)
        json_frame.rowconfigure(0, weight=1)
        
        self.json_text = scrolledtext.ScrolledText(json_frame, height=15, width=80)
        self.json_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def refresh_installed(self):
        """Refresh installed distributions data."""
        def refresh_thread():
            try:
                self.status_var.set("Loading installed distributions...")
                parser = WSLParser()
                distributions = parser.get_distributions()
                
                # Clear existing data
                for item in self.installed_tree.get_children():
                    self.installed_tree.delete(item)
                
                # Add new data
                for dist in distributions:
                    default_text = "Yes" if dist.is_default else "No"
                    self.installed_tree.insert('', 'end', values=(
                        dist.name,
                        dist.state,
                        dist.version,
                        default_text
                    ))
                
                # Update summary
                total = len(distributions)
                running = len(parser.get_running_distributions())
                stopped = len(parser.get_stopped_distributions())
                default_dist = parser.get_default_distribution()
                default_name = default_dist.name if default_dist else "None"
                
                summary = f"Total: {total} | Running: {running} | Stopped: {stopped} | Default: {default_name}"
                self.installed_summary_var.set(summary)
                
                self.status_var.set("Installed distributions loaded successfully")
                
            except Exception as e:
                self.status_var.set(f"Error loading installed distributions: {e}")
                messagebox.showerror("Error", f"Failed to load installed distributions:\n{e}")
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def refresh_available(self):
        """Refresh available distributions data."""
        def refresh_thread():
            try:
                self.status_var.set("Loading available distributions...")
                parser = WSLOnlineParser()
                distributions = parser.get_online_distributions()
                
                # Clear existing data
                for item in self.available_tree.get_children():
                    self.available_tree.delete(item)
                
                # Add new data
                for dist in distributions:
                    install_cmd = f"wsl --install {dist.name}"
                    self.available_tree.insert('', 'end', values=(
                        dist.name,
                        dist.friendly_name,
                        install_cmd
                    ))
                
                # Update summary
                total = len(distributions)
                ubuntu_count = len(parser.get_ubuntu_distributions())
                enterprise_count = len(parser.get_enterprise_distributions())
                
                summary = f"Total: {total} | Ubuntu variants: {ubuntu_count} | Enterprise: {enterprise_count}"
                self.available_summary_var.set(summary)
                
                self.status_var.set("Available distributions loaded successfully")
                
            except Exception as e:
                self.status_var.set(f"Error loading available distributions: {e}")
                messagebox.showerror("Error", f"Failed to load available distributions:\n{e}")
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def refresh_data(self):
        """Refresh all data."""
        self.refresh_installed()
        self.refresh_available()
    
    def export_to_json(self):
        """Export data to JSON format."""
        try:
            # Get data from both parsers
            installed_parser = WSLParser()
            available_parser = WSLOnlineParser()
            
            installed_data = installed_parser.to_dict()
            available_data = available_parser.to_dict()
            
            # Combine data
            export_data = {
                "installed_distributions": installed_data,
                "available_distributions": available_data,
                "summary": {
                    "installed_count": len(installed_data),
                    "available_count": len(available_data)
                }
            }
            
            # Update JSON text area
            json_output = json.dumps(export_data, indent=2)
            self.json_text.delete(1.0, tk.END)
            self.json_text.insert(1.0, json_output)
            
            self.status_var.set("Data exported to JSON successfully")
            
        except Exception as e:
            self.status_var.set(f"Error exporting data: {e}")
            messagebox.showerror("Error", f"Failed to export data:\n{e}")
    
    def show_help(self):
        """Show help dialog."""
        help_text = """
WSL Manager GUI Help

This application provides a graphical interface for managing WSL distributions.

Tabs:
• Installed Distributions: Shows currently installed WSL distributions
• Available Distributions: Shows distributions available for installation
• Actions & Info: Provides additional functionality and JSON export

Features:
• Refresh data from WSL commands
• View distribution details in organized tables
• Export data to JSON format
• Real-time status updates

Commands:
• Refresh: Updates the data in the current tab
• Refresh All Data: Updates data in all tabs
• Export to JSON: Exports all data to JSON format

For command-line usage, run:
python main.py help
        """
        
        messagebox.showinfo("WSL Manager Help", help_text)
    
    def on_distribution_select(self, event):
        """Handle distribution selection in the treeview."""
        selection = self.installed_tree.selection()
        if selection:
            self.rename_button.config(state='normal')
            self.delete_button.config(state='normal')
        else:
            self.rename_button.config(state='disabled')
            self.delete_button.config(state='disabled')
    
    def delete_selected_distribution(self):
        """Delete the selected WSL distribution."""
        selection = self.installed_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a distribution to delete.")
            return
        
        # Get the selected item
        item = selection[0]
        values = self.installed_tree.item(item, 'values')
        dist_name = values[0]  # Name is the first column
        
        # Show confirmation dialog
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the WSL distribution '{dist_name}'?\n\n"
            "This action cannot be undone and will permanently remove the distribution and all its data.",
            icon='warning'
        )
        
        if result:
            def delete_thread():
                try:
                    self.status_var.set(f"Deleting distribution '{dist_name}'...")
                    
                    # Create parser and delete the distribution
                    parser = WSLParser()
                    parser.delete_distribution(dist_name)
                    
                    # Refresh the installed distributions list
                    self.refresh_installed()
                    
                    self.status_var.set(f"Distribution '{dist_name}' deleted successfully")
                    messagebox.showinfo("Success", f"Distribution '{dist_name}' has been deleted successfully.")
                    
                except Exception as e:
                    self.status_var.set(f"Error deleting distribution: {e}")
                    messagebox.showerror("Error", f"Failed to delete distribution '{dist_name}':\n{e}")
            
            threading.Thread(target=delete_thread, daemon=True).start()
    
    def rename_selected_distribution(self):
        """Rename the selected WSL distribution."""
        selection = self.installed_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a distribution to rename.")
            return
        
        # Get the selected item
        item = selection[0]
        values = self.installed_tree.item(item, 'values')
        dist_name = values[0]  # Name is the first column
        
        # Show rename dialog
        new_name = self.show_rename_dialog(dist_name)
        if new_name is None:  # User cancelled
            return
        
        # Show confirmation dialog
        result = messagebox.askyesno(
            "Confirm Rename",
            f"Are you sure you want to rename '{dist_name}' to '{new_name}'?\n\n"
            "This will export and re-import the distribution, which may take a few minutes.",
            icon='question'
        )
        
        if result:
            def rename_thread():
                try:
                    self.status_var.set(f"Renaming distribution '{dist_name}' to '{new_name}'...")
                    
                    # Create parser and rename the distribution
                    parser = WSLParser()
                    parser.rename_distribution(dist_name, new_name)
                    
                    # Refresh the installed distributions list
                    self.refresh_installed()
                    
                    self.status_var.set(f"Distribution '{dist_name}' renamed to '{new_name}' successfully")
                    messagebox.showinfo("Success", f"Distribution '{dist_name}' has been renamed to '{new_name}' successfully.")
                    
                except Exception as e:
                    self.status_var.set(f"Error renaming distribution: {e}")
                    messagebox.showerror("Error", f"Failed to rename distribution '{dist_name}':\n{e}")
            
            threading.Thread(target=rename_thread, daemon=True).start()
    
    def show_rename_dialog(self, current_name):
        """Show dialog to get new name for distribution rename."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Rename Distribution")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        result = {'new_name': None}
        
        # Main frame
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"Rename {current_name}", style='Header.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Current name label
        current_label = ttk.Label(main_frame, text=f"Current name: {current_name}")
        current_label.pack(pady=(0, 10))
        
        # New name frame
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(name_frame, text="New name:").pack(anchor=tk.W)
        new_name_var = tk.StringVar()
        new_name_entry = ttk.Entry(name_frame, textvariable=new_name_var, width=30)
        new_name_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Help text
        help_label = ttk.Label(name_frame, text="Name can only contain letters, numbers, hyphens, and underscores", font=('Arial', 8))
        help_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Note about rename process
        note_label = ttk.Label(name_frame, text="Note: Renaming uses export/import process (may take a few minutes)", font=('Arial', 8), foreground='gray')
        note_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        def on_rename():
            new_name = new_name_var.get().strip()
            if not new_name:
                messagebox.showerror("Invalid Name", "Please enter a new name.")
                return
            
            if new_name == current_name:
                messagebox.showerror("Invalid Name", "New name must be different from current name.")
                return
            
            # Validate new name (basic validation)
            if not new_name.replace('-', '').replace('_', '').isalnum():
                messagebox.showerror("Invalid Name", "New name can only contain letters, numbers, hyphens, and underscores.")
                return
            
            result['new_name'] = new_name
            dialog.destroy()
        
        def on_cancel():
            result['new_name'] = None
            dialog.destroy()
        
        ttk.Button(buttons_frame, text="Rename", command=on_rename).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(buttons_frame, text="Cancel", command=on_cancel).pack(side=tk.RIGHT)
        
        # Focus on the entry field
        new_name_entry.focus()
        
        # Handle Enter key
        new_name_entry.bind('<Return>', lambda e: on_rename())
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result['new_name']
    
    def on_available_distribution_select(self, event):
        """Handle distribution selection in the available distributions treeview."""
        selection = self.available_tree.selection()
        if selection:
            self.install_button.config(state='normal')
        else:
            self.install_button.config(state='disabled')
    
    def install_selected_distribution(self):
        """Install the selected WSL distribution with optional custom name."""
        selection = self.available_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a distribution to install.")
            return
        
        # Get the selected item
        item = selection[0]
        values = self.available_tree.item(item, 'values')
        dist_name = values[0]  # Name is the first column
        friendly_name = values[1]  # Friendly name is the second column
        
        # Show custom name dialog
        custom_name = self.show_custom_name_dialog(dist_name, friendly_name)
        if custom_name is None:  # User cancelled
            return
        
        # Show confirmation dialog
        if custom_name:
            confirm_msg = f"Install '{friendly_name}' with custom name '{custom_name}'?"
        else:
            confirm_msg = f"Install '{friendly_name}' with default name '{dist_name}'?"
        
        result = messagebox.askyesno(
            "Confirm Installation",
            f"{confirm_msg}\n\nThis will download and install the distribution. This may take several minutes.",
            icon='question'
        )
        
        if result:
            def install_thread():
                try:
                    if custom_name:
                        self.status_var.set(f"Installing '{friendly_name}' as '{custom_name}'...")
                    else:
                        self.status_var.set(f"Installing '{friendly_name}'...")
                    
                    # Create parser and install the distribution
                    parser = WSLOnlineParser()
                    parser.install_distribution(dist_name, custom_name)
                    
                    # Refresh both installed and available distributions lists
                    self.refresh_installed()
                    self.refresh_available()
                    
                    if custom_name:
                        self.status_var.set(f"Distribution '{friendly_name}' installed as '{custom_name}' successfully")
                        messagebox.showinfo("Success", f"Distribution '{friendly_name}' has been installed as '{custom_name}' successfully.")
                    else:
                        self.status_var.set(f"Distribution '{friendly_name}' installed successfully")
                        messagebox.showinfo("Success", f"Distribution '{friendly_name}' has been installed successfully.")
                    
                except Exception as e:
                    self.status_var.set(f"Error installing distribution: {e}")
                    messagebox.showerror("Error", f"Failed to install distribution '{friendly_name}':\n{e}")
            
            threading.Thread(target=install_thread, daemon=True).start()
    
    def show_custom_name_dialog(self, dist_name, friendly_name):
        """Show dialog to get custom name for distribution installation."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Install Distribution")
        dialog.geometry("400x220")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        result = {'custom_name': None}
        
        # Main frame
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"Install {friendly_name}", style='Header.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Info label
        info_label = ttk.Label(main_frame, text=f"Distribution: {dist_name}")
        info_label.pack(pady=(0, 10))
        
        # Custom name frame
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(name_frame, text="Custom Name (optional):").pack(anchor=tk.W)
        custom_name_var = tk.StringVar()
        custom_name_entry = ttk.Entry(name_frame, textvariable=custom_name_var, width=30)
        custom_name_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Help text
        help_label = ttk.Label(name_frame, text="Leave empty to use default name", font=('Arial', 8))
        help_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Note about custom naming process
        note_label = ttk.Label(name_frame, text="Note: Custom naming uses export/import process (may take longer)", font=('Arial', 8), foreground='gray')
        note_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        def on_install():
            custom_name = custom_name_var.get().strip()
            if custom_name:
                # Validate custom name (basic validation)
                if not custom_name.replace('-', '').replace('_', '').isalnum():
                    messagebox.showerror("Invalid Name", "Custom name can only contain letters, numbers, hyphens, and underscores.")
                    return
                result['custom_name'] = custom_name
            else:
                result['custom_name'] = ""  # Empty string means use default
            dialog.destroy()
        
        def on_cancel():
            result['custom_name'] = None
            dialog.destroy()
        
        ttk.Button(buttons_frame, text="Install", command=on_install).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(buttons_frame, text="Cancel", command=on_cancel).pack(side=tk.RIGHT)
        
        # Focus on the entry field
        custom_name_entry.focus()
        
        # Handle Enter key
        custom_name_entry.bind('<Return>', lambda e: on_install())
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result['custom_name']


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
