#!/usr/bin/env python3
"""
Environment Check Script for Travel Database Project
This script verifies that your environment is correctly configured.
"""

import sys
import os
import subprocess
import platform
import shutil

# Terminal colors for better readability
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_status(message, status, details=None):
    """Print a status message with color coding"""
    if status == "OK":
        status_str = f"{Colors.GREEN}✓ {status}{Colors.END}"
    elif status == "WARNING":
        status_str = f"{Colors.YELLOW}⚠ {status}{Colors.END}"
    elif status == "ERROR":
        status_str = f"{Colors.RED}✗ {status}{Colors.END}"
    else:
        status_str = status
    
    print(f"{message}: {status_str}")
    if details:
        print(f"  {Colors.BLUE}{details}{Colors.END}")
    print()

def check_python_version():
    """Check Python version"""
    required_version = (3, 6)
    current_version = sys.version_info
    
    if current_version.major < required_version[0] or \
       (current_version.major == required_version[0] and current_version.minor < required_version[1]):
        print_status("Python Version", "ERROR", 
                    f"Found {current_version.major}.{current_version.minor}, but {required_version[0]}.{required_version[1]}+ is required")
        return False
    else:
        print_status("Python Version", "OK", 
                    f"Found {current_version.major}.{current_version.minor}.{current_version.micro}")
        return True

def check_docker():
    """Check if Docker is installed and running"""
    docker_path = shutil.which('docker')
    
    if not docker_path:
        print_status("Docker Installation", "ERROR", "Docker not found. Please install Docker Desktop.")
        return False
    
    try:
        result = subprocess.run(['docker', 'info'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True, 
                               check=False)
        if result.returncode != 0:
            print_status("Docker Status", "ERROR", "Docker is installed but not running. Please start Docker Desktop.")
            return False
        else:
            print_status("Docker Status", "OK", "Docker is running")
            return True
    except Exception as e:
        print_status("Docker Status", "ERROR", f"Error checking Docker: {str(e)}")
        return False

def check_required_packages():
    """Check if required Python packages are installed"""
    required_packages = {
        'pandas': 'Data manipulation library',
        'matplotlib': 'Visualization library',
        'seaborn': 'Advanced visualization library',
        'sqlalchemy': 'SQL toolkit and ORM',
        'mysql-connector-python': 'MySQL connector',
        'faker': 'Fake data generation',
        'openpyxl': 'Excel file handling'
    }
    
    missing_packages = []
    installed_packages = []
    
    for package, description in required_packages.items():
        try:
            __import__(package)
            installed_packages.append(f"{package} ({description})")
        except ImportError:
            missing_packages.append(f"{package} ({description})")
    
    if missing_packages:
        print_status("Python Packages", "WARNING", 
                    "Missing packages: " + ", ".join(missing_packages))
        return False
    else:
        print_status("Python Packages", "OK", 
                    "All required packages are installed")
        return True

def check_file_structure():
    """Check if required files exist"""
    required_files = [
        'schema.sql',
        'seed_db.py',
        'make_reports.py',
        'advanced_reports.py',
        'run_all.sh',
        'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print_status("File Structure", "ERROR", 
                    "Missing files: " + ", ".join(missing_files))
        return False
    else:
        print_status("File Structure", "OK", 
                    "All required files are present")
        return True

def check_scripts_executable():
    """Check if shell scripts are executable"""
    shell_scripts = [
        'run_all.sh',
        'setup_all.sh',
        'start_db.sh',
        'install_report_deps.sh'
    ]
    
    not_executable = []
    
    for script in shell_scripts:
        if os.path.exists(script) and not os.access(script, os.X_OK):
            not_executable.append(script)
    
    if not_executable:
        print_status("Script Permissions", "WARNING", 
                    "Non-executable scripts: " + ", ".join(not_executable) + 
                    "\nRun: chmod +x *.sh")
        return False
    else:
        print_status("Script Permissions", "OK", 
                    "All shell scripts are executable")
        return True

def print_summary(results):
    """Print a summary of all checks"""
    print("\n" + "="*50)
    print(f"{Colors.BOLD}ENVIRONMENT CHECK SUMMARY{Colors.END}")
    print("="*50)
    
    all_ok = all(results.values())
    
    if all_ok:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Your environment is ready!{Colors.END}")
        print(f"\nRun {Colors.BLUE}./run_all.sh{Colors.END} to set up the project.")
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Your environment needs some adjustments{Colors.END}")
        print("\nPlease fix the issues above before proceeding.")
        
        if not results.get('docker', True):
            print(f"\n{Colors.BLUE}➤ Install Docker Desktop:{Colors.END}")
            print("   https://www.docker.com/products/docker-desktop")
        
        if not results.get('packages', True):
            print(f"\n{Colors.BLUE}➤ Install missing Python packages:{Colors.END}")
            print("   pip install pandas matplotlib seaborn sqlalchemy mysql-connector-python faker openpyxl")
        
        if not results.get('permissions', True):
            print(f"\n{Colors.BLUE}➤ Make scripts executable:{Colors.END}")
            print("   chmod +x *.sh")
    
    print("\nFor detailed setup instructions, see README.md or GETTING_STARTED.md")
    print("="*50 + "\n")

def main():
    """Run all environment checks"""
    print(f"\n{Colors.BOLD}Travel Database Project - Environment Check{Colors.END}\n")
    
    results = {}
    
    # Check Python version
    results['python'] = check_python_version()
    
    # Check Docker
    results['docker'] = check_docker()
    
    # Check required packages
    results['packages'] = check_required_packages()
    
    # Check file structure
    results['files'] = check_file_structure()
    
    # Check script permissions
    results['permissions'] = check_scripts_executable()
    
    # Print summary
    print_summary(results)

if __name__ == "__main__":
    main() 