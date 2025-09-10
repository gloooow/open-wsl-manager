# Console Window Fix

## Problem
When clicking buttons in the WSL Manager GUI, random CMD windows would flash briefly for a few milliseconds. This was happening because subprocess calls were using the default behavior which shows console windows.

## Solution
Created a new utility module `src/subprocess_utils.py` that wraps subprocess calls with Windows-specific flags to suppress console windows.

### Changes Made

1. **Created `src/subprocess_utils.py`**
   - `run_wsl_command()` - For WSL-specific commands
   - `run_command_silent()` - For general commands
   - Both use `subprocess.CREATE_NO_WINDOW` flag on Windows

2. **Updated `src/wsl_parser.py`**
   - Replaced all `subprocess.run()` calls with `run_wsl_command()`
   - Affects: `get_wsl_output()`, `delete_distribution()`, `rename_distribution()`

3. **Updated `src/wsl_online_parser.py`**
   - Replaced all `subprocess.run()` calls with `run_wsl_command()`
   - Affects: `get_wsl_online_output()`, `install_distribution()`, `_install_with_custom_name()`

4. **Updated `build.py`**
   - Added `CREATE_NO_WINDOW` flag to build process subprocess calls

## How It Works

The `CREATE_NO_WINDOW` flag is a Windows-specific subprocess flag that:
- Prevents console windows from appearing
- Runs commands in the background silently
- Maintains all functionality while hiding the console

## Testing

To test the fix:

1. **Rebuild your executables:**
   ```bash
   python build.py
   ```

2. **Test the GUI:**
   - Launch `WSLManagerGUI.exe`
   - Click any button (Refresh, Delete, Install, etc.)
   - No console windows should flash

3. **Test the CLI:**
   - Run `WSLManager.exe installed`
   - Run `WSLManager.exe available`
   - Commands should work normally without console flashing

## Compatibility

- **Windows:** Console windows are suppressed
- **Linux/macOS:** No change in behavior (flag is ignored)
- **All functionality preserved:** Commands work exactly the same

## Files Modified

- `src/subprocess_utils.py` (new)
- `src/wsl_parser.py`
- `src/wsl_online_parser.py`
- `build.py`
- `BUILD_INSTRUCTIONS.md` (documentation)

The fix is backward compatible and doesn't affect the core functionality of the WSL Manager application.
