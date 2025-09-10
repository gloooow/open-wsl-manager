#!/usr/bin/env python3
"""
Example usage of the WSL Parser

This script demonstrates how to use the WSLParser class to get information
about WSL distributions.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from wsl_parser import WSLParser

def main():
    """Example usage of the WSL parser."""
    # Create a parser instance
    parser = WSLParser()
    
    try:
        # Get all distributions
        distributions = parser.get_distributions()
        
        print("=== WSL Distribution Information ===")
        print(f"Total distributions found: {len(distributions)}")
        print()
        
        # Print each distribution
        for i, dist in enumerate(distributions, 1):
            print(f"Distribution {i}:")
            print(f"  Name: {dist.name}")
            print(f"  State: {dist.state}")
            print(f"  Version: {dist.version}")
            print(f"  Is Default: {dist.is_default}")
            print()
        
        # Get specific information
        default_dist = parser.get_default_distribution()
        if default_dist:
            print(f"Default distribution: {default_dist.name}")
        
        running_dists = parser.get_running_distributions()
        print(f"Running distributions: {[d.name for d in running_dists]}")
        
        stopped_dists = parser.get_stopped_distributions()
        print(f"Stopped distributions: {[d.name for d in stopped_dists]}")
        
        # Get JSON output
        print("\n=== JSON Output ===")
        print(parser.to_json())
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
