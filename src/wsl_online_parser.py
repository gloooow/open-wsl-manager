#!/usr/bin/env python3
"""
WSL Online Distributions Parser

A Python application that parses the output from 'wsl --list --online' command
and provides structured data about available WSL distributions that can be installed.
"""

import subprocess
import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class WSLOnlineDistribution:
    """Represents an available WSL distribution that can be installed."""
    name: str
    friendly_name: str


class WSLOnlineParser:
    """Parser for WSL online distribution information."""
    
    def __init__(self):
        self.distributions: List[WSLOnlineDistribution] = []
    
    def get_wsl_online_output(self) -> str:
        """Execute 'wsl --list --online' command and return the output."""
        try:
            result = subprocess.run(
                ['wsl', '--list', '--online'],
                capture_output=True,
                check=True
            )
            # WSL output is in UTF-16 LE encoding without BOM
            return result.stdout.decode('utf-16le')
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to execute wsl command: {e}")
        except FileNotFoundError:
            raise RuntimeError("WSL command not found. Make sure WSL is installed.")
    
    def parse_wsl_online_output(self, output: str) -> List[WSLOnlineDistribution]:
        """Parse the output from 'wsl --list --online' command."""
        lines = output.strip().split('\n')
        
        if len(lines) < 3:
            return []
        
        distributions = []
        
        # Find the header line and start parsing from the next line
        header_found = False
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Look for the header line with "NAME" and "FRIENDLY NAME"
            if "NAME" in line and "FRIENDLY NAME" in line:
                header_found = True
                continue
            
            # Skip empty lines and the introductory text
            if not line or not header_found:
                continue
            
            # Skip lines that don't look like distribution entries
            if line.startswith("The following") or line.startswith("Install using"):
                continue
            
            # Parse the distribution line
            # The format is: NAME                            FRIENDLY NAME
            # We need to split on the boundary between the two columns
            
            # Find the position where the friendly name starts
            # The friendly name typically starts after a long sequence of spaces
            parts = line.split()
            
            if len(parts) >= 2:
                # The first part is the name, the rest is the friendly name
                name = parts[0]
                friendly_name = ' '.join(parts[1:])
                
                distribution = WSLOnlineDistribution(
                    name=name,
                    friendly_name=friendly_name
                )
                distributions.append(distribution)
        
        self.distributions = distributions
        return distributions
    
    def get_online_distributions(self) -> List[WSLOnlineDistribution]:
        """Get available WSL distributions by running the command and parsing output."""
        output = self.get_wsl_online_output()
        return self.parse_wsl_online_output(output)
    
    def get_distribution_by_name(self, name: str) -> Optional[WSLOnlineDistribution]:
        """Get a specific distribution by name."""
        for dist in self.distributions:
            if dist.name.lower() == name.lower():
                return dist
        return None
    
    def search_distributions(self, search_term: str) -> List[WSLOnlineDistribution]:
        """Search distributions by name or friendly name."""
        search_term = search_term.lower()
        results = []
        
        for dist in self.distributions:
            if (search_term in dist.name.lower() or 
                search_term in dist.friendly_name.lower()):
                results.append(dist)
        
        return results
    
    def get_ubuntu_distributions(self) -> List[WSLOnlineDistribution]:
        """Get all Ubuntu distributions."""
        return self.search_distributions("ubuntu")
    
    def get_enterprise_distributions(self) -> List[WSLOnlineDistribution]:
        """Get enterprise distributions (SUSE, Oracle, etc.)."""
        enterprise_keywords = ["enterprise", "oracle", "suse"]
        results = []
        
        for dist in self.distributions:
            for keyword in enterprise_keywords:
                if keyword in dist.name.lower() or keyword in dist.friendly_name.lower():
                    results.append(dist)
                    break
        
        return results
    
    def to_dict(self) -> List[Dict]:
        """Convert distributions to list of dictionaries."""
        return [asdict(dist) for dist in self.distributions]
    
    def to_json(self, indent: int = 2) -> str:
        """Convert distributions to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def print_summary(self):
        """Print a formatted summary of available WSL distributions."""
        if not self.distributions:
            print("No available WSL distributions found.")
            return
        
        print(f"Found {len(self.distributions)} available WSL distribution(s):")
        print("-" * 80)
        print(f"{'Name':<30} {'Friendly Name':<45}")
        print("-" * 80)
        
        for dist in self.distributions:
            print(f"{dist.name:<30} {dist.friendly_name:<45}")
        
        print("-" * 80)
    
    def print_install_commands(self):
        """Print the install commands for all distributions."""
        if not self.distributions:
            print("No available WSL distributions found.")
            return
        
        print("Install commands for available distributions:")
        print("-" * 50)
        
        for dist in self.distributions:
            print(f"wsl --install {dist.name}")
        
        print("-" * 50)
    
    def install_distribution(self, distribution_name: str, custom_name: str = None) -> bool:
        """Install a WSL distribution with an optional custom name."""
        try:
            # Ensure distributions are loaded
            if not self.distributions:
                self.get_online_distributions()
            
            # Check if the distribution exists in available distributions
            dist = self.get_distribution_by_name(distribution_name)
            if not dist:
                raise ValueError(f"Distribution '{distribution_name}' not found in available distributions")
            
            if custom_name and custom_name.strip():
                # For custom names, we need to use a different approach
                # First install with default name, then export and import with custom name
                return self._install_with_custom_name(distribution_name, custom_name)
            else:
                # Standard install command
                install_cmd = ['wsl', '--install', distribution_name]
                
                # Execute the install command
                result = subprocess.run(
                    install_cmd,
                    capture_output=True,
                    check=True,
                    text=True
                )
                
                return True
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if isinstance(e.stderr, str) else e.stderr.decode('utf-8', errors='ignore')
            raise RuntimeError(f"Failed to install distribution '{distribution_name}': {error_msg}")
        except Exception as e:
            raise RuntimeError(f"Error installing distribution '{distribution_name}': {e}")
    
    def _install_with_custom_name(self, distribution_name: str, custom_name: str) -> bool:
        """Install a distribution with a custom name using export/import method."""
        import tempfile
        import time
        
        try:
            # Step 1: Install with default name (no-launch to avoid opening terminal)
            print(f"Installing {distribution_name} with default name...")
            install_cmd = ['wsl', '--install', distribution_name, '--no-launch']
            subprocess.run(install_cmd, capture_output=True, check=True, text=True)
            
            # Step 2: Wait for installation to complete
            print("Waiting for installation to complete...")
            time.sleep(5)
            
            # Step 3: Export the distribution to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.tar', delete=False) as temp_file:
                temp_path = temp_file.name
            
            print(f"Exporting {distribution_name} to temporary file...")
            export_cmd = ['wsl', '--export', distribution_name, temp_path]
            subprocess.run(export_cmd, capture_output=True, check=True, text=True)
            
            # Step 4: Import with custom name
            print(f"Importing as {custom_name}...")
            import_location = f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Packages\\CanonicalGroupLimited.{custom_name}_79rhkp1fndgsc\\LocalState"
            
            # Create the directory if it doesn't exist
            os.makedirs(import_location, exist_ok=True)
            
            import_cmd = ['wsl', '--import', custom_name, import_location, temp_path]
            subprocess.run(import_cmd, capture_output=True, check=True, text=True)
            
            # Step 5: Unregister the original distribution
            print(f"Removing original {distribution_name}...")
            unregister_cmd = ['wsl', '--unregister', distribution_name]
            subprocess.run(unregister_cmd, capture_output=True, check=True, text=True)
            
            # Step 6: Clean up temporary file
            os.unlink(temp_path)
            
            print(f"Successfully installed {distribution_name} as {custom_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if isinstance(e.stderr, str) else e.stderr.decode('utf-8', errors='ignore')
            raise RuntimeError(f"Failed to install with custom name: {error_msg}")
        except Exception as e:
            raise RuntimeError(f"Error installing with custom name: {e}")
        finally:
            # Clean up temporary file if it exists
            try:
                if 'temp_path' in locals():
                    os.unlink(temp_path)
            except:
                pass


def main():
    """Main function to demonstrate the WSL online parser."""
    parser = WSLOnlineParser()
    
    try:
        # Get and parse available WSL distributions
        distributions = parser.get_online_distributions()
        
        # Print summary
        parser.print_summary()
        
        # Print install commands
        print("\n")
        parser.print_install_commands()
        
        # Print JSON output
        print("\nJSON Output:")
        print(parser.to_json())
        
        # Demonstrate some utility methods
        ubuntu_dists = parser.get_ubuntu_distributions()
        print(f"\nUbuntu distributions: {len(ubuntu_dists)}")
        for dist in ubuntu_dists:
            print(f"  - {dist.name}: {dist.friendly_name}")
        
        enterprise_dists = parser.get_enterprise_distributions()
        print(f"\nEnterprise distributions: {len(enterprise_dists)}")
        for dist in enterprise_dists:
            print(f"  - {dist.name}: {dist.friendly_name}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
