# Building WSL Manager Executables

## Quick Build

**Windows:**

```bash
build.bat
```

**Cross-platform:**

```bash
python build.py
```

## What You Get

- `WSLManager.exe` - Command-line interface
- `WSLManagerGUI.exe` - Graphical interface
- Both are standalone (no Python required)

## Requirements

- Python 3.7+
- Windows 10/11 with WSL

## Output

Executables will be created in:

- `dist/` - Build output
- `release/` - Distribution package

See `BUILD_INSTRUCTIONS.md` for detailed information.
