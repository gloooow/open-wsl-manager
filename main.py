#!/usr/bin/env python3
"""
WSL Manager - Main Entry Point

A unified interface for managing WSL distributions.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.wsl_parser import WSLParser
from src.wsl_online_parser import WSLOnlineParser


def show_installed_distributions():
    """Show currently installed WSL distributions."""
    print("=== Installed WSL Distributions ===")
    parser = WSLParser()
    
    try:
        distributions = parser.get_distributions()
        parser.print_summary()
        
        if distributions:
            print(f"\nTotal: {len(distributions)} distribution(s)")
            default_dist = parser.get_default_distribution()
            if default_dist:
                print(f"Default: {default_dist.name}")
            
            running = parser.get_running_distributions()
            stopped = parser.get_stopped_distributions()
            print(f"Running: {len(running)}, Stopped: {len(stopped)}")
        
    except Exception as e:
        print(f"Error: {e}")


def show_available_distributions():
    """Show available WSL distributions that can be installed."""
    print("=== Available WSL Distributions ===")
    parser = WSLOnlineParser()
    
    try:
        distributions = parser.get_online_distributions()
        parser.print_summary()
        
        if distributions:
            print(f"\nTotal: {len(distributions)} distribution(s) available")
            
            # Show categories
            ubuntu_dists = parser.get_ubuntu_distributions()
            enterprise_dists = parser.get_enterprise_distributions()
            
            print(f"Ubuntu variants: {len(ubuntu_dists)}")
            print(f"Enterprise distributions: {len(enterprise_dists)}")
            
            print("\nQuick install commands:")
            print("Ubuntu: wsl --install Ubuntu")
            print("Debian: wsl --install Debian")
            print("Kali: wsl --install kali-linux")
            print("Arch: wsl --install archlinux")
        
    except Exception as e:
        print(f"Error: {e}")


def show_help():
    """Show help information."""
    print("WSL Manager - WSL Distribution Management Tool")
    print("=" * 50)
    print("Usage: python main.py [command]")
    print()
    print("Commands:")
    print("  installed    Show currently installed WSL distributions")
    print("  available    Show available WSL distributions to install")
    print("  gui          Launch the graphical user interface")
    print("  help         Show this help message")
    print()
    print("Examples:")
    print("  python main.py installed")
    print("  python main.py available")
    print("  python main.py gui")
    print()
    print("For more detailed examples, see the files in the 'examples' directory.")


def launch_gui():
    """Launch the GUI application."""
    try:
        import gui
        gui.main()
    except ImportError as e:
        print(f"Error launching GUI: {e}")
        print("Make sure tkinter is installed and gui.py is in the current directory.")
    except Exception as e:
        print(f"Error launching GUI: {e}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "installed":
        show_installed_distributions()
    elif command == "available":
        show_available_distributions()
    elif command == "gui":
        launch_gui()
    elif command in ["help", "-h", "--help"]:
        show_help()
    else:
        print(f"Unknown command: {command}")
        print("Use 'python main.py help' for available commands.")


if __name__ == "__main__":
    main()
