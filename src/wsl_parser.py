#!/usr/bin/env python3
"""
WSL Distribution Parser

A Python application that parses the output from 'wsl -l -v' command
and provides structured data about WSL distributions.
"""

import subprocess
import re
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class WSLDistribution:
    """Represents a WSL distribution with its properties."""
    name: str
    state: str
    version: str
    is_default: bool = False


class WSLParser:
    """Parser for WSL distribution information."""
    
    def __init__(self):
        self.distributions: List[WSLDistribution] = []
    
    def get_wsl_output(self) -> str:
        """Execute 'wsl -l -v' command and return the output."""
        try:
            result = subprocess.run(
                ['wsl', '-l', '-v'],
                capture_output=True,
                check=True
            )
            # WSL output is in UTF-16 LE encoding without BOM
            return result.stdout.decode('utf-16le')
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to execute wsl command: {e}")
        except FileNotFoundError:
            raise RuntimeError("WSL command not found. Make sure WSL is installed.")
    
    def parse_wsl_output(self, output: str) -> List[WSLDistribution]:
        """Parse the output from 'wsl -l -v' command."""
        # Handle Windows line endings properly
        lines = output.strip().replace('\r\n', '\n').replace('\r', '\n').split('\n')
        
        if len(lines) < 2:
            return []
        
        # Skip the header line
        data_lines = lines[1:]
        
        distributions = []
        
        for line in data_lines:
            line = line.rstrip()  # Remove trailing whitespace but keep leading
            if not line:
                continue
            
            # Check if this is the default distribution (marked with *)
            is_default = line.startswith('*')
            if is_default:
                line = line[1:]  # Remove the asterisk but keep the space
            
            # The output uses fixed-width columns
            # Based on the header: "  NAME             STATE           VERSION"
            # Let's use a more flexible approach to find column boundaries
            
            # Find the start of each column by looking for the header pattern
            # NAME starts after the initial spaces, STATE and VERSION follow
            parts = line.split()
            
            if len(parts) >= 3:
                # The first part after * (if present) is the name
                # The last two parts are state and version
                name = parts[0]
                state = parts[-2]
                version = parts[-1]
            else:
                # Fallback to fixed-width parsing if split doesn't work
                # NAME starts at position 2, STATE at position 18, VERSION at position 34
                name = line[2:18].strip()
                state = line[18:34].strip()
                version = line[34:].strip()
            
            # Only add if we have valid data
            if name and state and version:
                distribution = WSLDistribution(
                    name=name,
                    state=state,
                    version=version,
                    is_default=is_default
                )
                distributions.append(distribution)
        
        self.distributions = distributions
        return distributions
    
    def get_distributions(self) -> List[WSLDistribution]:
        """Get WSL distributions by running the command and parsing output."""
        output = self.get_wsl_output()
        return self.parse_wsl_output(output)
    
    def get_distribution_by_name(self, name: str) -> Optional[WSLDistribution]:
        """Get a specific distribution by name."""
        for dist in self.distributions:
            if dist.name == name:
                return dist
        return None
    
    def get_default_distribution(self) -> Optional[WSLDistribution]:
        """Get the default WSL distribution."""
        for dist in self.distributions:
            if dist.is_default:
                return dist
        return None
    
    def get_running_distributions(self) -> List[WSLDistribution]:
        """Get all running WSL distributions."""
        return [dist for dist in self.distributions if dist.state.lower() == 'running']
    
    def get_stopped_distributions(self) -> List[WSLDistribution]:
        """Get all stopped WSL distributions."""
        return [dist for dist in self.distributions if dist.state.lower() == 'stopped']
    
    def to_dict(self) -> List[Dict]:
        """Convert distributions to list of dictionaries."""
        return [asdict(dist) for dist in self.distributions]
    
    def to_json(self, indent: int = 2) -> str:
        """Convert distributions to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def delete_distribution(self, name: str) -> bool:
        """Delete a WSL distribution by name."""
        try:
            # First, ensure distributions are loaded and check if the distribution exists
            self.get_distributions()  # This populates self.distributions
            dist = self.get_distribution_by_name(name)
            if not dist:
                raise ValueError(f"Distribution '{name}' not found")
            
            # Execute the unregister command
            result = subprocess.run(
                ['wsl', '--unregister', name],
                capture_output=True,
                check=True
            )
            
            # Refresh the distributions list after deletion
            self.get_distributions()
            
            return True
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to delete distribution '{name}': {e.stderr.decode()}")
        except Exception as e:
            raise RuntimeError(f"Error deleting distribution '{name}': {e}")
    
    def rename_distribution(self, old_name: str, new_name: str) -> bool:
        """Rename a WSL distribution using export/import method."""
        import tempfile
        import time
        import os
        
        try:
            # First, ensure distributions are loaded and check if the distribution exists
            self.get_distributions()  # This populates self.distributions
            dist = self.get_distribution_by_name(old_name)
            if not dist:
                raise ValueError(f"Distribution '{old_name}' not found")
            
            # Check if new name already exists
            existing_dist = self.get_distribution_by_name(new_name)
            if existing_dist:
                raise ValueError(f"Distribution '{new_name}' already exists")
            
            # Validate new name (basic validation)
            if not new_name.replace('-', '').replace('_', '').isalnum():
                raise ValueError("New name can only contain letters, numbers, hyphens, and underscores")
            
            # Step 1: Export the distribution to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.tar', delete=False) as temp_file:
                temp_path = temp_file.name
            
            print(f"Exporting {old_name} to temporary file...")
            export_cmd = ['wsl', '--export', old_name, temp_path]
            subprocess.run(export_cmd, capture_output=True, check=True, text=True)
            
            # Step 2: Import with new name
            print(f"Importing as {new_name}...")
            import_location = f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Packages\\CanonicalGroupLimited.{new_name}_79rhkp1fndgsc\\LocalState"
            
            # Create the directory if it doesn't exist
            os.makedirs(import_location, exist_ok=True)
            
            import_cmd = ['wsl', '--import', new_name, import_location, temp_path]
            subprocess.run(import_cmd, capture_output=True, check=True, text=True)
            
            # Step 3: Unregister the original distribution
            print(f"Removing original {old_name}...")
            unregister_cmd = ['wsl', '--unregister', old_name]
            subprocess.run(unregister_cmd, capture_output=True, check=True, text=True)
            
            # Step 4: Clean up temporary file
            os.unlink(temp_path)
            
            # Step 5: Refresh the distributions list
            self.get_distributions()
            
            print(f"Successfully renamed {old_name} to {new_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if isinstance(e.stderr, str) else e.stderr.decode('utf-8', errors='ignore')
            raise RuntimeError(f"Failed to rename distribution: {error_msg}")
        except Exception as e:
            raise RuntimeError(f"Error renaming distribution: {e}")
        finally:
            # Clean up temporary file if it exists
            try:
                if 'temp_path' in locals():
                    os.unlink(temp_path)
            except:
                pass
    
    def print_summary(self):
        """Print a formatted summary of WSL distributions."""
        if not self.distributions:
            print("No WSL distributions found.")
            return
        
        print(f"Found {len(self.distributions)} WSL distribution(s):")
        print("-" * 60)
        
        for dist in self.distributions:
            default_marker = " (DEFAULT)" if dist.is_default else ""
            print(f"Name: {dist.name}{default_marker}")
            print(f"State: {dist.state}")
            print(f"Version: {dist.version}")
            print("-" * 60)


def main():
    """Main function to demonstrate the WSL parser."""
    parser = WSLParser()
    
    try:
        # Get and parse WSL distributions
        distributions = parser.get_distributions()
        
        # Print summary
        parser.print_summary()
        
        # Print JSON output
        print("\nJSON Output:")
        print(parser.to_json())
        
        # Demonstrate some utility methods
        default_dist = parser.get_default_distribution()
        if default_dist:
            print(f"\nDefault distribution: {default_dist.name}")
        
        running_dists = parser.get_running_distributions()
        print(f"Running distributions: {len(running_dists)}")
        
        stopped_dists = parser.get_stopped_distributions()
        print(f"Stopped distributions: {len(stopped_dists)}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

