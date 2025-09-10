"""
Subprocess utilities for WSL Manager

Provides a wrapper for subprocess calls that suppresses console windows on Windows.
"""

import subprocess
import sys
import os
from typing import List, Optional, Union


def run_wsl_command(
    args: List[str], 
    capture_output: bool = True, 
    check: bool = True,
    text: bool = False,
    **kwargs
) -> subprocess.CompletedProcess:
    """
    Run a WSL command with proper console window suppression on Windows.
    
    Args:
        args: Command arguments (e.g., ['wsl', '-l', '-v'])
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit code
        text: Whether to return text instead of bytes
        **kwargs: Additional arguments for subprocess.run
    
    Returns:
        CompletedProcess object
    """
    # Add Windows-specific flags to suppress console window
    if sys.platform == "win32":
        kwargs.setdefault('creationflags', subprocess.CREATE_NO_WINDOW)
    
    return subprocess.run(
        args,
        capture_output=capture_output,
        check=check,
        text=text,
        **kwargs
    )


def run_command_silent(
    command: Union[str, List[str]], 
    shell: bool = False,
    capture_output: bool = True, 
    check: bool = True,
    text: bool = False,
    **kwargs
) -> subprocess.CompletedProcess:
    """
    Run any command with proper console window suppression on Windows.
    
    Args:
        command: Command to run (string or list)
        shell: Whether to use shell
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit code
        text: Whether to return text instead of bytes
        **kwargs: Additional arguments for subprocess.run
    
    Returns:
        CompletedProcess object
    """
    # Add Windows-specific flags to suppress console window
    if sys.platform == "win32":
        kwargs.setdefault('creationflags', subprocess.CREATE_NO_WINDOW)
    
    return subprocess.run(
        command,
        shell=shell,
        capture_output=capture_output,
        check=check,
        text=text,
        **kwargs
    )
