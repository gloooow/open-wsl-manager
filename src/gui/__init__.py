"""
GUI package for WSL Manager.

This package contains all GUI-related components organized into separate modules.
"""

from .main_window import WSLManagerGUI
from .tabs import InstalledTab, AvailableTab, ActionsTab
from .dialogs import RenameDialog, InstallDialog, HelpDialog
from .widgets import DistributionTreeView, ActionButtons, StatusBar
from .models import DistributionViewModel, TabState, DistributionSummary, AvailableDistributionSummary, ExportData
from .actions import WSLManagerActions

__all__ = [
    'WSLManagerGUI',
    'InstalledTab', 
    'AvailableTab', 
    'ActionsTab',
    'RenameDialog',
    'InstallDialog', 
    'HelpDialog',
    'DistributionTreeView',
    'ActionButtons',
    'StatusBar',
    'DistributionViewModel',
    'TabState',
    'DistributionSummary',
    'AvailableDistributionSummary',
    'ExportData',
    'WSLManagerActions'
]
