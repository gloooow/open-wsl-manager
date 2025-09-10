#!/usr/bin/env python3
"""
Setup script for WSL Manager
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "WSL Manager - A tool for managing WSL distributions"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="wsl-manager",
    version="1.0.0",
    author="Stefan",
    description="A comprehensive tool for managing WSL distributions",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/open-wsl-manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "build": [
            "pyinstaller>=5.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wsl-manager=wsl_manager.cli:main",
            "wsl-manager-gui=wsl_manager.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "wsl_manager": [
            "assets/*.ico",
            "assets/*.png",
        ],
    },
)
