"""
WSL Manager - A comprehensive tool for managing WSL distributions.

This package provides both command-line and graphical interfaces for managing
Windows Subsystem for Linux (WSL) distributions.
"""

__version__ = "1.0.0"
__author__ = "Stefan Cula"
__email__ = "stefanncula@gmail.com"

from .core.parser import WSLParser
from .core.online_parser import WSLOnlineParser

__all__ = [
    "WSLParser",
    "WSLOnlineParser",
    "__version__",
    "__author__",
    "__email__",
]
