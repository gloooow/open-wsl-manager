"""
Configuration and constants for the GUI application.
"""

# Window configuration
WINDOW_TITLE = "Open WSL Manager"
WINDOW_SIZE = "1000x700"  # Increased width for better table display
MIN_WINDOW_SIZE = (1000, 600)  # Increased minimum width

# Style configuration
STYLES = {
    'title': 'Title.TLabel',
    'header': 'Header.TLabel', 
    'status': 'Status.TLabel',
    'primary_button': 'Primary.TButton',
    'secondary_button': 'Secondary.TButton',
    'danger_button': 'Danger.TButton',
    'success_button': 'Success.TButton',
    'notebook': 'Modern.TNotebook',
    'tab': 'Modern.TNotebook.Tab',
    'modern_frame': 'Modern.TFrame'
}

# Font configuration
FONTS = {
    'title': ('Segoe UI', 16, 'bold'),
    'header': ('Segoe UI', 12, 'bold'),
    'status': ('Segoe UI', 10),
    'help': ('Segoe UI', 8),
    'button': ('Segoe UI', 9, 'normal'),
    'tab': ('Segoe UI', 10, 'normal')
}

# Modern color scheme
COLORS = {
    'primary': '#0078d4',      # Microsoft blue
    'primary_hover': '#106ebe', # Darker blue for hover
    'secondary': '#6c757d',    # Gray
    'secondary_hover': '#5a6268', # Darker gray for hover
    'success': '#28a745',      # Green
    'success_hover': '#218838', # Darker green for hover
    'danger': '#dc3545',       # Red
    'danger_hover': '#c82333', # Darker red for hover
    'background': '#ffffff',   # White background for cleaner look
    'text': '#212529',         # Dark text
    'border': '#dee2e6',       # Light border
    'tab_active': '#ffffff',   # White for active tab
    'tab_inactive': '#f0f0f0', # Very light gray for inactive tabs
    'tab_border': '#d0d0d0',   # Light gray tab border color
    'tab_text_active': '#000000', # Black text for active tab
    'tab_text_inactive': '#666666', # Dark gray text for inactive tabs
    'button_text_disabled': '#999999' # Light gray text for disabled buttons
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
        'Name': 300,  # Increased for longer distribution names
        'State': 120,  # Increased for better readability
        'Version': 120,  # Increased for version info
        'Default': 100   # Increased for better alignment
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
        'Name': 250,  # Increased for distribution names
        'Friendly Name': 300,  # Increased for friendly names
        'Install Command': 250  # Increased for install commands
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
