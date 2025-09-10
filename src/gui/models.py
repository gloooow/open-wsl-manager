"""
Data models and view models for the WSL Manager GUI.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from ..wsl_parser import WSLDistribution
from ..wsl_online_parser import WSLOnlineDistribution


@dataclass
class DistributionSummary:
    """Summary information for distributions."""
    total: int
    running: int
    stopped: int
    default_name: str


@dataclass
class AvailableDistributionSummary:
    """Summary information for available distributions."""
    total: int
    ubuntu_count: int
    enterprise_count: int


@dataclass
class ExportData:
    """Data structure for JSON export."""
    installed_distributions: List[Dict[str, Any]]
    available_distributions: List[Dict[str, Any]]
    summary: Dict[str, int]


class DistributionViewModel:
    """View model for distribution data."""
    
    def __init__(self):
        self.installed_distributions: List[WSLDistribution] = []
        self.available_distributions: List[WSLOnlineDistribution] = []
    
    def update_installed(self, distributions: List[WSLDistribution]):
        """Update installed distributions data."""
        self.installed_distributions = distributions
    
    def update_available(self, distributions: List[WSLOnlineDistribution]):
        """Update available distributions data."""
        self.available_distributions = distributions
    
    def get_installed_summary(self) -> DistributionSummary:
        """Get summary of installed distributions."""
        total = len(self.installed_distributions)
        running = len([d for d in self.installed_distributions if d.state.lower() == 'running'])
        stopped = len([d for d in self.installed_distributions if d.state.lower() == 'stopped'])
        default_dist = next((d for d in self.installed_distributions if d.is_default), None)
        default_name = default_dist.name if default_dist else "None"
        
        return DistributionSummary(total, running, stopped, default_name)
    
    def get_available_summary(self) -> AvailableDistributionSummary:
        """Get summary of available distributions."""
        total = len(self.available_distributions)
        ubuntu_count = len([d for d in self.available_distributions if 'ubuntu' in d.name.lower()])
        enterprise_count = len([d for d in self.available_distributions 
                               if any(keyword in d.name.lower() or keyword in d.friendly_name.lower() 
                                     for keyword in ['enterprise', 'oracle', 'suse'])])
        
        return AvailableDistributionSummary(total, ubuntu_count, enterprise_count)
    
    def get_export_data(self) -> ExportData:
        """Get data for JSON export."""
        from dataclasses import asdict
        
        installed_data = [asdict(dist) for dist in self.installed_distributions]
        available_data = [asdict(dist) for dist in self.available_distributions]
        
        summary = {
            "installed_count": len(installed_data),
            "available_count": len(available_data)
        }
        
        return ExportData(installed_data, available_data, summary)
    
    def find_installed_by_name(self, name: str) -> Optional[WSLDistribution]:
        """Find an installed distribution by name."""
        return next((d for d in self.installed_distributions if d.name == name), None)
    
    def find_available_by_name(self, name: str) -> Optional[WSLOnlineDistribution]:
        """Find an available distribution by name."""
        return next((d for d in self.available_distributions if d.name.lower() == name.lower()), None)


class TabState:
    """State management for tabs."""
    
    def __init__(self):
        self.selected_installed: Optional[str] = None
        self.selected_available: Optional[tuple] = None
        self.is_loading_installed: bool = False
        self.is_loading_available: bool = False
    
    def set_selected_installed(self, name: Optional[str]):
        """Set the selected installed distribution."""
        self.selected_installed = name
    
    def set_selected_available(self, selection: Optional[tuple]):
        """Set the selected available distribution."""
        self.selected_available = selection
    
    def set_loading_installed(self, loading: bool):
        """Set the loading state for installed distributions."""
        self.is_loading_installed = loading
    
    def set_loading_available(self, loading: bool):
        """Set the loading state for available distributions."""
        self.is_loading_available = loading
    
    def can_delete(self) -> bool:
        """Check if delete action is available."""
        return self.selected_installed is not None and not self.is_loading_installed
    
    def can_rename(self) -> bool:
        """Check if rename action is available."""
        return self.selected_installed is not None and not self.is_loading_installed
    
    def can_install(self) -> bool:
        """Check if install action is available."""
        return self.selected_available is not None and not self.is_loading_available
