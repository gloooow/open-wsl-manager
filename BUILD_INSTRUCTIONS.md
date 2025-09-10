# WSL Manager - Build Instructions

This document explains how to create standalone executables for the WSL Manager application.

## Prerequisites

- Python 3.7 or higher
- Windows 10/11 (for WSL functionality)
- WSL installed and configured
- (Optional) Pillow library for icon creation: `pip install Pillow`

## Quick Start

### Option 1: Automated Build (Recommended)

1. **Create an icon (optional but recommended):**

   ```bash
   python create_icon.py
   ```

2. **Run the build script:**

   ```bash
   python build.py
   ```

   Or on Windows, simply double-click:

   ```bash
   build.bat
   ```

3. **Find your executables:**
   - CLI version: `dist/WSLManager.exe`
   - GUI version: `dist/WSLManagerGUI.exe`
   - Release package: `release/` directory

### Option 2: Manual Build

1. **Install PyInstaller:**

   ```bash
   pip install pyinstaller
   ```

2. **Build CLI executable:**

   ```bash
   pyinstaller wsl_manager_cli.spec
   ```

3. **Build GUI executable:**

   ```bash
   pyinstaller wsl_manager_gui.spec
   ```

## Build Output

After a successful build, you'll find:

```text
dist/
├── WSLManager.exe      # CLI executable
└── WSLManagerGUI.exe   # GUI executable

release/
├── WSLManager.exe      # CLI executable (copy)
├── WSLManagerGUI.exe   # GUI executable (copy)
└── README.txt          # Usage instructions
```

## Executable Features

### CLI Executable (`WSLManager.exe`)

- **Size:** ~15-20 MB
- **Console:** Yes (shows command output)
- **Usage:**

  ```bash
  WSLManager.exe installed    # Show installed distributions
  WSLManager.exe available    # Show available distributions
  WSLManager.exe help         # Show help
  ```

### GUI Executable (`WSLManagerGUI.exe`)

- **Size:** ~20-25 MB
- **Console:** No (windowed application)
- **Usage:** Double-click to launch

## Distribution

### Standalone Distribution

The executables are completely standalone and include:

- Python runtime
- All required libraries
- Application code

**Requirements for end users:**

- Windows 10/11
- WSL installed
- No Python installation required

### File Sizes

- CLI: ~15-20 MB
- GUI: ~20-25 MB
- Total release package: ~40-50 MB

## Troubleshooting

### Common Issues

1. **"PyInstaller not found"**

   ```bash
   pip install pyinstaller
   ```

2. **"Module not found" errors**

   - Ensure you're running from the project root directory
   - Check that all source files are present

3. **Large executable size**

   - This is normal for PyInstaller builds
   - The executable includes the entire Python runtime

4. **Antivirus warnings**

   - Some antivirus software may flag PyInstaller executables
   - This is a false positive - add to exclusions if needed

5. **Console windows flashing briefly**

   - This has been fixed in the latest version
   - All subprocess calls now use `CREATE_NO_WINDOW` flag on Windows
   - Rebuild your executables to get the fix

### Build Optimization

To reduce executable size, you can modify the `.spec` files:

1. **Exclude unnecessary modules:**

   ```python
   excludes=['matplotlib', 'numpy', 'pandas']  # Add to excludes list
   ```

2. **Use UPX compression:**

   ```python
   upx=True  # Already enabled in our spec files
   ```

3. **One-file vs one-directory:**

   - Current setup: One-file (easier distribution)
   - Alternative: One-directory (faster startup, larger distribution)

## Advanced Configuration

### Custom Icons

#### Automatic Icon Creation

The easiest way to add an icon:

```bash
python create_icon.py
```

This will create a simple WSL-themed icon automatically.

#### Manual Icon Setup

To use your own custom icon:

1. **Create or obtain an `.ico` file:**

   - Use online converters (PNG/JPG → ICO)
   - Create with image editors (GIMP, Paint.NET)
   - Download from icon websites

2. **Save as `icon.ico` in the project root**

3. **The build process will automatically use it**

#### Icon Requirements

- **Format:** `.ico` file
- **Sizes:** Multiple sizes recommended (16x16, 32x32, 48x48, 64x64, 128x128, 256x256)
- **Location:** `icon.ico` in the project root directory

#### No Icon

If you don't want a custom icon:

1. Edit the `.spec` files and set `icon=None`
2. Or simply don't create an `icon.ico` file (build will warn but continue)

### Version Information

To add version information to Windows executables:

1. Create a version file (e.g., `version.txt`)
2. Update the spec files:

   ```python
   version='version.txt'
   ```

### Code Signing

For production distribution, consider code signing:

1. Obtain a code signing certificate
2. Update the spec files:

   ```python
   codesign_identity='Your Certificate Name'
   ```

## Development vs Production Builds

### Development Builds

- Include debug information
- Larger file sizes
- Better error reporting

### Production Builds

- Optimized for size
- No debug information
- Better performance

To create production builds, modify the spec files:

```python
debug=False
strip=True
upx=True
```

## Testing Executables

Before distribution, test your executables:

1. **Test on clean system:**

   - Install on Windows without Python
   - Verify WSL functionality

2. **Test all features:**

   - CLI commands
   - GUI functionality
   - Error handling

3. **Performance testing:**

   - Startup time
   - Memory usage
   - Response time

## Support

If you encounter issues:

1. Check the build logs in the console output
2. Verify all dependencies are installed
3. Ensure you're using a compatible Python version
4. Check that WSL is properly installed and configured

## License

The build process and executables follow the same license as the source code.
