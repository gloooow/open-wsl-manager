# WSL Manager

A comprehensive tool for managing Windows Subsystem for Linux (WSL) distributions with both command-line and graphical interfaces.

## Features

- **List installed WSL distributions** with detailed information (name, state, version, default status)
- **List available WSL distributions** that can be installed from Microsoft Store
- **Delete WSL distributions** safely with confirmation
- **Rename WSL distributions** using export/import method
- **Install new WSL distributions** with optional custom names
- **Graphical user interface** for easy management
- **Command-line interface** for automation and scripting
- **Cross-platform compatibility** (Windows with WSL support)

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/open-wsl-manager.git
cd open-wsl-manager
```

2. Install the package:
```bash
pip install -e .
```

### Development Installation

1. Clone the repository and install in development mode:
```bash
git clone https://github.com/yourusername/open-wsl-manager.git
cd open-wsl-manager
pip install -e ".[build]"
```

## Usage

### Command Line Interface

After installation, you can use the `wsl-manager` command:

```bash
# Show installed WSL distributions
wsl-manager installed

# Show available WSL distributions to install
wsl-manager available

# Launch the graphical interface
wsl-manager gui

# Show help
wsl-manager help
```

### Legacy Entry Points

For backward compatibility, you can still use the old entry points:

```bash
# Using Python directly
python main.py installed
python main.py available
python main.py gui

# Launch GUI directly
python gui.py
python launch_gui.py
```

### Graphical User Interface

Launch the GUI application:

```bash
wsl-manager-gui
# or
wsl-manager gui
```

The GUI provides:
- Tabbed interface for installed and available distributions
- One-click actions (delete, rename, install)
- Real-time status updates
- Confirmation dialogs for destructive operations

### Python API

You can also use the WSL Manager as a Python library:

```python
from wsl_manager import WSLParser, WSLOnlineParser

# Get installed distributions
parser = WSLParser()
distributions = parser.get_distributions()
for dist in distributions:
    print(f"{dist.name}: {dist.state} ({dist.version})")

# Get available distributions
online_parser = WSLOnlineParser()
available = online_parser.get_online_distributions()
for dist in available:
    print(f"{dist.name}: {dist.friendly_name}")
```

## Project Structure

```
wsl_manager/
├── __init__.py              # Package initialization
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── parser.py           # WSL distribution parser
│   └── online_parser.py    # Online distribution parser
├── cli/                     # Command-line interface
│   ├── __init__.py
│   └── main.py             # CLI entry point
├── gui/                     # Graphical user interface
│   ├── __init__.py
│   ├── main_window.py      # Main GUI window
│   ├── tabs.py             # Tab components
│   ├── dialogs.py          # Dialog boxes
│   ├── actions.py          # Action handlers
│   ├── models.py           # Data models
│   ├── widgets.py          # Custom widgets
│   └── config.py           # GUI configuration
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── subprocess_utils.py # Subprocess management
└── assets/                  # Application assets
    ├── icon.ico
    └── icon.png
```

## Building Executables

To build standalone executables:

1. Install build dependencies:
```bash
pip install -e ".[build]"
```

2. Run the build script:
```bash
python build_scripts/build.py
```

The executables will be created in the `dist/` directory.

## Requirements

- Python 3.8 or higher
- Windows 10/11 with WSL installed
- tkinter (included with Python standard library)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 1.0.0
- Initial release
- Professional package structure
- Command-line and GUI interfaces
- WSL distribution management
- Cross-platform compatibility
