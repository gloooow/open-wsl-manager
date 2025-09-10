"""
Configuration and constants for the GUI application.
"""

# Window configuration
WINDOW_TITLE = "Open WSL Manager"
WINDOW_SIZE = "1000x700"
MIN_WINDOW_SIZE = (800, 600)

# Style configuration
STYLES = {
    'title': 'Title.TLabel',
    'header': 'Header.TLabel', 
    'status': 'Status.TLabel'
}

# Font configuration
FONTS = {
    'title': ('Arial', 16, 'bold'),
    'header': ('Arial', 12, 'bold'),
    'status': ('Arial', 10),
    'help': ('Arial', 8)
}

# Treeview column configurations
INSTALLED_COLUMNS = {
    'columns': ('Name', 'State', 'Version', 'Default'),
    'headings': {
        'Name': 'Distribution Name',
        'State': 'State', 
        'Version': 'WSL Version',
        'Default': 'Default'
    },
    'widths': {
        'Name': 200,
        'State': 100,
        'Version': 100,
        'Default': 80
    }
}

AVAILABLE_COLUMNS = {
    'columns': ('Name', 'Friendly Name', 'Install Command'),
    'headings': {
        'Name': 'Distribution Name',
        'Friendly Name': 'Friendly Name',
        'Install Command': 'Install Command'
    },
    'widths': {
        'Name': 200,
        'Friendly Name': 250,
        'Install Command': 200
    }
}

# Dialog configurations
DIALOG_CONFIGS = {
    'rename': {
        'title': 'Rename Distribution',
        'size': '400x200'
    },
    'install': {
        'title': 'Install Distribution', 
        'size': '400x220'
    }
}

# Help text
HELP_TEXT = """
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
