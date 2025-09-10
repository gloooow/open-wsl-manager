#!/usr/bin/env python3
"""
Example usage of the WSL Online Parser

This script demonstrates how to use the WSLOnlineParser class to get information
about available WSL distributions that can be installed.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from wsl_online_parser import WSLOnlineParser

def main():
    """Example usage of the WSL online parser."""
    # Create a parser instance
    parser = WSLOnlineParser()
    
    try:
        # Get all available distributions
        distributions = parser.get_online_distributions()
        
        print("=== Available WSL Distributions ===")
        print(f"Total distributions available: {len(distributions)}")
        print()
        
        # Print each distribution
        for i, dist in enumerate(distributions, 1):
            print(f"Distribution {i}:")
            print(f"  Name: {dist.name}")
            print(f"  Friendly Name: {dist.friendly_name}")
            print(f"  Install Command: wsl --install {dist.name}")
            print()
        
        # Get specific information
        print("=== Distribution Categories ===")
        
        # Get Ubuntu distributions
        ubuntu_dists = parser.get_ubuntu_distributions()
        print(f"Ubuntu distributions ({len(ubuntu_dists)}):")
        for dist in ubuntu_dists:
            print(f"  - {dist.name}: {dist.friendly_name}")
        print()
        
        # Get enterprise distributions
        enterprise_dists = parser.get_enterprise_distributions()
        print(f"Enterprise distributions ({len(enterprise_dists)}):")
        for dist in enterprise_dists:
            print(f"  - {dist.name}: {dist.friendly_name}")
        print()
        
        # Search for specific distributions
        print("=== Search Examples ===")
        
        # Search for Debian
        debian_results = parser.search_distributions("debian")
        print(f"Debian search results: {[d.name for d in debian_results]}")
        
        # Search for SUSE
        suse_results = parser.search_distributions("suse")
        print(f"SUSE search results: {[d.name for d in suse_results]}")
        
        # Search for Arch
        arch_results = parser.search_distributions("arch")
        print(f"Arch search results: {[d.name for d in arch_results]}")
        print()
        
        # Get specific distribution by name
        print("=== Get Specific Distribution ===")
        ubuntu_dist = parser.get_distribution_by_name("Ubuntu")
        if ubuntu_dist:
            print(f"Found Ubuntu: {ubuntu_dist.friendly_name}")
        
        kali_dist = parser.get_distribution_by_name("kali-linux")
        if kali_dist:
            print(f"Found Kali: {kali_dist.friendly_name}")
        print()
        
        # Print formatted summary
        print("=== Formatted Summary ===")
        parser.print_summary()
        
        # Print install commands
        print("\n=== Install Commands ===")
        parser.print_install_commands()
        
        # Get JSON output
        print("\n=== JSON Output ===")
        json_output = parser.to_json()
        print(json_output)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
