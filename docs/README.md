# WSL Distribution Parsers

Python applications that parse WSL command outputs and provide structured data about WSL distributions.

## Features

### Installed Distributions Parser (`wsl_parser.py`)

- Parses WSL distribution information from `wsl -l -v` command output
- Handles UTF-16 encoding properly (WSL outputs in UTF-16 LE)
- Identifies default distributions (marked with `*`)
- Provides structured data with distribution name, state, and version
- Includes utility methods for filtering distributions
- Exports data to JSON format
- Comprehensive error handling

### Online Distributions Parser (`wsl_online_parser.py`)

- Parses available WSL distributions from `wsl --list --online` command output
- Shows distributions that can be installed
- Provides distribution name and friendly name
- Includes search and filtering capabilities
- Generates install commands for each distribution
- Categorizes distributions (Ubuntu, Enterprise, etc.)
- Exports data to JSON format

## Installation

No external dependencies required. Uses only Python standard library modules.

```bash
# Clone or download the project
# No pip install needed
```

## Project Structure

```text
open-wsl-manager/
├── main.py                    # Main entry point (command-line interface)
├── gui.py                     # Graphical user interface
├── launch_gui.py              # Simple GUI launcher
├── requirements.txt           # Dependencies (none required)
├── src/                      # Source code
│   ├── __init__.py           # Package initialization
│   ├── wsl_parser.py         # Parser for installed WSL distributions
│   └── wsl_online_parser.py  # Parser for available WSL distributions
├── examples/                 # Example usage scripts
│   ├── example_usage.py      # Example for installed distributions
│   └── example_online_usage.py # Example for online distributions
└── docs/                     # Documentation
    └── README.md             # This file
```

## Usage

### Quick Start

```bash
# Launch the GUI (recommended)
python gui.py
# or
python main.py gui

# Command-line interface
python main.py installed    # Show installed distributions
python main.py available    # Show available distributions
python main.py help         # Show help
```

### Basic Usage

```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from wsl_parser import WSLParser
from wsl_online_parser import WSLOnlineParser

# Installed distributions
parser = WSLParser()
distributions = parser.get_distributions()
parser.print_summary()

# Available distributions
online_parser = WSLOnlineParser()
available = online_parser.get_online_distributions()
online_parser.print_summary()
```

### GUI Interface

The GUI provides a user-friendly interface with the following features:

- **Installed Distributions Tab**: View currently installed WSL distributions in a table format
- **Available Distributions Tab**: Browse and see install commands for available distributions
- **Actions & Info Tab**: Export data to JSON and access additional functionality
- **Real-time Updates**: Refresh data from WSL commands
- **Status Bar**: Shows current operation status

```bash
# Launch GUI
python gui.py

# Or use the main script
python main.py gui
```

### Running the Examples

```bash
# Run example for installed distributions
python examples/example_usage.py

# Run example for available distributions
python examples/example_online_usage.py
```

## Data Structure

Each WSL distribution is represented as a `WSLDistribution` object with the following properties:

- `name`: The name of the WSL distribution
- `state`: Current state (Running, Stopped, etc.)
- `version`: WSL version (1 or 2)
- `is_default`: Boolean indicating if this is the default distribution

## Example Output

```text
Found 1 WSL distribution(s):
------------------------------------------------------------
Name: natie-website (DEFAULT)
State: Stopped
Version: 2
------------------------------------------------------------

JSON Output:
[
  {
    "name": "natie-website",
    "state": "Stopped",
    "version": "2",
    "is_default": true
  }
]
```

## Error Handling

The parser includes comprehensive error handling for:

- WSL command not found
- Command execution failures
- Encoding issues
- Malformed output

## Requirements

- Python 3.6+
- Windows with WSL installed
- No external dependencies

## Files

- `wsl_parser.py`: Main parser class and functionality
- `example_usage.py`: Example script showing how to use the parser
- `requirements.txt`: Dependencies (none required)
- `README.md`: This documentation
