"""
Action handlers and business logic for the WSL Manager GUI.
"""

import threading
import json
from tkinter import messagebox
from typing import Callable, Optional

from ..core.parser import WSLParser, WSLDistribution
from ..core.online_parser import WSLOnlineParser, WSLOnlineDistribution
from .dialogs import RenameDialog, InstallDialog, HelpDialog
from .models import DistributionSummary, AvailableDistributionSummary


class WSLManagerActions:
    """Handles all business logic and actions for the WSL Manager GUI."""
    
    def __init__(self, status_callback: Callable[[str], None]):
        self.status_callback = status_callback
        self.help_dialog = HelpDialog(None)
    
    def refresh_installed_distributions(self, callback: Callable[[list, str], None]):
        """Refresh installed distributions data in a separate thread."""
        def refresh_thread():
            try:
                self.status_callback("Loading installed distributions...")
                parser = WSLParser()
                distributions = parser.get_distributions()
                
                # Calculate summary using model
                summary_obj = DistributionSummary(
                    total=len(distributions),
                    running=len(parser.get_running_distributions()),
                    stopped=len(parser.get_stopped_distributions()),
                    default_name=parser.get_default_distribution().name if parser.get_default_distribution() else "None"
                )
                
                summary = f"Total: {summary_obj.total} | Running: {summary_obj.running} | Stopped: {summary_obj.stopped} | Default: {summary_obj.default_name}"
                
                self.status_callback("Installed distributions loaded successfully")
                callback(distributions, summary)
                
            except Exception as e:
                self.status_callback(f"Error loading installed distributions: {e}")
                messagebox.showerror("Error", f"Failed to load installed distributions:\n{e}")
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def refresh_available_distributions(self, callback: Callable[[list, str], None]):
        """Refresh available distributions data in a separate thread."""
        def refresh_thread():
            try:
                self.status_callback("Loading available distributions...")
                parser = WSLOnlineParser()
                distributions = parser.get_online_distributions()
                
                # Calculate summary using model
                summary_obj = AvailableDistributionSummary(
                    total=len(distributions),
                    ubuntu_count=len(parser.get_ubuntu_distributions()),
                    enterprise_count=len(parser.get_enterprise_distributions())
                )
                
                summary = f"Total: {summary_obj.total} | Ubuntu variants: {summary_obj.ubuntu_count} | Enterprise: {summary_obj.enterprise_count}"
                
                self.status_callback("Available distributions loaded successfully")
                callback(distributions, summary)
                
            except Exception as e:
                self.status_callback(f"Error loading available distributions: {e}")
                messagebox.showerror("Error", f"Failed to load available distributions:\n{e}")
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def delete_distribution(self, name: str, callback: Callable[[], None]):
        """Delete a WSL distribution in a separate thread."""
        def delete_thread():
            try:
                self.status_callback(f"Deleting distribution '{name}'...")
                
                # Create parser and delete the distribution
                parser = WSLParser()
                parser.delete_distribution(name)
                
                self.status_callback(f"Distribution '{name}' deleted successfully")
                messagebox.showinfo("Success", f"Distribution '{name}' has been deleted successfully.")
                callback()
                
            except Exception as e:
                self.status_callback(f"Error deleting distribution: {e}")
                messagebox.showerror("Error", f"Failed to delete distribution '{name}':\n{e}")
        
        threading.Thread(target=delete_thread, daemon=True).start()
    
    def rename_distribution(self, old_name: str, new_name: str, callback: Callable[[], None]):
        """Rename a WSL distribution in a separate thread."""
        def rename_thread():
            try:
                self.status_callback(f"Renaming distribution '{old_name}' to '{new_name}'...")
                
                # Create parser and rename the distribution
                parser = WSLParser()
                parser.rename_distribution(old_name, new_name)
                
                self.status_callback(f"Distribution '{old_name}' renamed to '{new_name}' successfully")
                messagebox.showinfo("Success", f"Distribution '{old_name}' has been renamed to '{new_name}' successfully.")
                callback()
                
            except Exception as e:
                self.status_callback(f"Error renaming distribution: {e}")
                messagebox.showerror("Error", f"Failed to rename distribution '{old_name}':\n{e}")
        
        threading.Thread(target=rename_thread, daemon=True).start()
    
    def install_distribution(self, dist_name: str, friendly_name: str, custom_name: Optional[str], callback: Callable[[], None]):
        """Install a WSL distribution in a separate thread."""
        def install_thread():
            try:
                if custom_name:
                    self.status_callback(f"Installing '{friendly_name}' as '{custom_name}'...")
                else:
                    self.status_callback(f"Installing '{friendly_name}'...")
                
                # Create parser and install the distribution
                parser = WSLOnlineParser()
                parser.install_distribution(dist_name, custom_name)
                
                if custom_name:
                    self.status_callback(f"Distribution '{friendly_name}' installed as '{custom_name}' successfully")
                    messagebox.showinfo("Success", f"Distribution '{friendly_name}' has been installed as '{custom_name}' successfully.")
                else:
                    self.status_callback(f"Distribution '{friendly_name}' installed successfully")
                    messagebox.showinfo("Success", f"Distribution '{friendly_name}' has been installed successfully.")
                
                callback()
                
            except Exception as e:
                self.status_callback(f"Error installing distribution: {e}")
                messagebox.showerror("Error", f"Failed to install distribution '{friendly_name}':\n{e}")
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def export_to_json(self, callback: Callable[[str], None]):
        """Export data to JSON format."""
        try:
            # Get data from both parsers
            installed_parser = WSLParser()
            available_parser = WSLOnlineParser()
            
            installed_data = installed_parser.to_dict()
            available_data = available_parser.to_dict()
            
            # Combine data using model
            from .models import ExportData
            export_data = ExportData(
                installed_distributions=installed_data,
                available_distributions=available_data,
                summary={
                    "installed_count": len(installed_data),
                    "available_count": len(available_data)
                }
            )
            
            # Convert to JSON
            json_output = json.dumps(export_data.__dict__, indent=2)
            
            self.status_callback("Data exported to JSON successfully")
            callback(json_output)
            
        except Exception as e:
            self.status_callback(f"Error exporting data: {e}")
            messagebox.showerror("Error", f"Failed to export data:\n{e}")
    
    def show_rename_dialog(self, parent, current_name: str) -> Optional[str]:
        """Show rename dialog and return the new name."""
        dialog = RenameDialog(parent, current_name)
        return dialog.show()
    
    def show_install_dialog(self, parent, dist_name: str, friendly_name: str) -> Optional[str]:
        """Show install dialog and return the custom name."""
        dialog = InstallDialog(parent, dist_name, friendly_name)
        return dialog.show()
    
    def show_help_dialog(self, parent):
        """Show help dialog."""
        self.help_dialog.parent = parent
        self.help_dialog.show()
    
    def confirm_action(self, title: str, message: str, icon: str = 'question') -> bool:
        """Show confirmation dialog and return the result."""
        return messagebox.askyesno(title, message, icon=icon)
    
    def show_warning(self, title: str, message: str):
        """Show warning dialog."""
        messagebox.showwarning(title, message)
